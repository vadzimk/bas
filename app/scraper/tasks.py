import asyncio
import os

from celery import Celery
from playwright.async_api import async_playwright

from app.models import Job
from app.scraper.LinkedinSearch import LinkedinSearch
from app import db, celery, create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')  # access  flask-sqlalchemy


# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/


async def async_task(search_fields):
    """
    :param search_fields: dictionary of search fields
    :return: None - result of the task is stored in db
    """
    print('starting search', search_fields)
    new_search = LinkedinSearch(**search_fields)  # TODO need to sanitize user input
    async with async_playwright() as pwt:
        browser = await pwt.chromium.launch(args=[''],
                                            headless=False,
                                            slow_mo=100
                                            )
        bpage = await browser.new_page()
        with app.app_context():
            bpage = await new_search.create_session(bpage)  # one session for each task
            await new_search.populate(bpage)  # TODO update state here
            await asyncio.sleep(1)

            # delete duplicate rows in db https://stackoverflow.com/a/3317575/5320906
            # Create a query that identifies the row for each domain with the lowest id
            inner_q = db.session.query(db.func.min(Job.id)).group_by(Job.description_text, Job.title, Job.company_id)
            aliased = db.alias(inner_q)
            # Select the rows that do not match the subquery
            q = db.session.query(Job).filter(~Job.id.in_(aliased))

            # Delete the unmatched rows (SQLAlchemy generates a single DELETE statement from this loop)
            for job in q:
                db.session.delete(job)
            db.session.commit()


@celery.task()
def scrape_linkedin(search_fields: dict):
    """    :param search_fields:
    :param self: celery sets this argument
    """
    asyncio.run(async_task(search_fields))
