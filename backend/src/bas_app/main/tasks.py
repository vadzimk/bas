import asyncio
import logging
import os
from enum import Enum

from celery import shared_task
from playwright.async_api import async_playwright
from playwright.async_api._generated import Page as PlayWrightPage

from ..models import Job
from ..scraper.IndeedSearch import IndeedSearch
from ..scraper.LinkedinSearch import LinkedinSearch
from .. import db, create_app


# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/


async def async_task(search_fields, linkedin_credentials, task_update_state):
    """
    :param linkedin_credentials:
    :param search_fields: dictionary of search fields
    :return: None - result of the task is stored in db
    because of how celery.Task is configured we don't need the app_context() here
    """
    print('starting search', search_fields)
    new_search = LinkedinSearch(**search_fields, linkedin_credentials=linkedin_credentials)  # TODO need to sanitize user input
    async with async_playwright() as pwt:
        browser = await pwt.chromium.launch(args=[''],
                                            headless=False,
                                            slow_mo=100
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
def scrape_linkedin(self, search_fields: dict, linkedin_credentials: dict):
    """
    :param linkedin_credentials: fake username and password for scraping
    :param search_fields: for linkedin search
    :param self: celery sets this argument
    """
    result = asyncio.run(async_task(
        search_fields=convert_search_fields(search_fields, 'linkedin'),
        linkedin_credentials=linkedin_credentials,
        task_update_state=self.update_state
    ))
    # https://docs.celeryq.dev/en/latest/userguide/tasks.html#success
    return result


def convert_search_fields(input_fields: dict, job_board: str):
    """ converts search field values to the enum values that a particular search can accept
     including the experience filed that is either an array or a single value
    examples can be found in the test_tasks.py file
     """
    reference = {
        'linkedin': {
            'radius': {
                'all': LinkedinSearch.Filters.Radius.ALL,
                'exact': LinkedinSearch.Filters.Radius.EXACT,
                '5mi': LinkedinSearch.Filters.Radius.FIVE,
                '10mi': LinkedinSearch.Filters.Radius.TEN,
                '25mi': LinkedinSearch.Filters.Radius.TWENTY_FIVE,
                '50': LinkedinSearch.Filters.Radius.FIFTY
            },
            'experience': {
                'all': LinkedinSearch.Filters.Experience.ALL,
                'internship': LinkedinSearch.Filters.Experience.INTERNSHIP,
                'entry level': LinkedinSearch.Filters.Experience.ENTRY_LEVEL,
                'associate': LinkedinSearch.Filters.Experience.ASSOCIATE,
                'mid-senior': LinkedinSearch.Filters.Experience.MID_SENIOR,
                'director': LinkedinSearch.Filters.Experience.DIRECTOR,
                'executive': LinkedinSearch.Filters.Experience.EXECUTIVE
            },
            'age': {
                'all': LinkedinSearch.Filters.Age.ALL,
                'month': LinkedinSearch.Filters.Age.PAST_MONTH,
                'week': LinkedinSearch.Filters.Age.PAST_WEEK,
                'day': LinkedinSearch.Filters.Age.PAST_24H
            }
        },
        'indeed': {
            'radius': {
                'all': IndeedSearch.Filters.Radius.ALL,
                'exact': IndeedSearch.Filters.Radius.EXACT,
                '5mi': IndeedSearch.Filters.Radius.FIVE,
                '10mi': IndeedSearch.Filters.Radius.TEN,
                '15mi': IndeedSearch.Filters.Radius.FIFTEEN,
                '25mi': IndeedSearch.Filters.Radius.TWENTY_FIVE,
                '100mi': IndeedSearch.Filters.Radius.HUNDRED,
            },
            'experience': {
                'all': IndeedSearch.Filters.Experience.ALL,
                'entry level': IndeedSearch.Filters.Experience.ENTRY,
                'mid': IndeedSearch.Filters.Experience.MID,
                'senior': IndeedSearch.Filters.Experience.SENIOR,
            },
            'age': {
                'all': IndeedSearch.Filters.Age.ALL,
                '1 day': IndeedSearch.Filters.Age.ONE,
                '3 days': IndeedSearch.Filters.Age.TREE,
                '7 days': IndeedSearch.Filters.Age.SEVEN,
                '14 days': IndeedSearch.Filters.Age.FOURTEEN,
            },
            'education': {
                'school': IndeedSearch.Filters.Education.SCHOOL,
                'associates': IndeedSearch.Filters.Education.ASSOCIATES,
                'bachelors': IndeedSearch.Filters.Education.BACHELORS,
                'masters': IndeedSearch.Filters.Education.MASTERS,
            }
        }
    }
    result = {}
    for k, v in input_fields.items():
        if k in reference[job_board].keys():
            if k == 'experience' and job_board == 'linkedin':
                experience = [reference[job_board][k][exp] for exp in input_fields[k]]
                result[k] = experience
            else:
                result[k] = reference[job_board][k][v]

        else:
            result[k] = v
    return result
