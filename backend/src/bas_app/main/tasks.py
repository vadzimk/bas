import asyncio
import logging
import os

from celery import shared_task
from playwright.async_api import async_playwright
from playwright.async_api._generated import Page as PlayWrightPage

from ..models import Job
from ..scraper.LinkedinSearch import LinkedinSearch
from .. import db, create_app


# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/


async def async_task(search_fields, task_update_state):
    """
    :param search_fields: dictionary of search fields
    :return: None - result of the task is stored in db
    because of how celery.Task is configured we don't need the app_context() here
    """
    print('starting search', search_fields)
    new_search = LinkedinSearch(**search_fields)  # TODO need to sanitize user input
    async with async_playwright() as pwt:
        browser = await pwt.chromium.launch(args=[''],
                                            # headless=False,
                                            # slow_mo=100
                                            )
        bpage: PlayWrightPage = await browser.new_page()

        bpage: PlayWrightPage = await new_search.create_session(bpage)  # one session for each task
        task_update_state(state='BEGUN')
        await new_search.populate(bpage=bpage, task_update_state=task_update_state)  # TODO update state here

        # delete duplicate rows in db https://stackoverflow.com/a/3317575/5320906
        # Create a query that identifies the row for each domain with the lowest id
        inner_q = db.session.query(db.func.min(Job.id)).group_by(Job.description_text, Job.title, Job.company_id)
        aliased = db.alias(inner_q)
        # Select the rows that do not match the subquery
        q = db.session.query(Job).filter(~Job.id.in_(aliased))

        # Delete the unmatched rows (SQLAlchemy generates a single DELETE statement from this loop)
        count_deleted = 0
        for job in q:
            db.session.delete(job)
            count_deleted += 1
        db.session.commit()
        new_duplicates_value = new_search.meta['job_duplicates_current'] + count_deleted

        meta = new_search.meta.copy()
        meta.update(job_duplicates_total=new_duplicates_value)
        return meta


@shared_task(bind=True)
def scrape_linkedin(self, search_fields: dict):
    """    :param search_fields:
    :param self: celery sets this argument
    """
    result = asyncio.run(async_task(search_fields=search_fields, task_update_state=self.update_state))
    # https://docs.celeryq.dev/en/latest/userguide/tasks.html#success
    return result
