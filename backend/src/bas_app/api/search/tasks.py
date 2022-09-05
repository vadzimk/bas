import asyncio
import logging
import os
from enum import Enum
from typing import Type

from celery import shared_task
from celery.result import AsyncResult
from playwright.async_api import async_playwright
from playwright.async_api._generated import Page as PlayWrightPage

from bas_app.models import Job
from bas_app.scraper.BaseSearch import BaseSearch
from bas_app.scraper.IndeedSearch import IndeedSearch
from bas_app.scraper.LinkedinSearch import LinkedinSearch
from bas_app import db, create_app


# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/


async def async_task(new_search: Type[BaseSearch], task_update_state: callable):
    """
    :param new_search: LinkedinSearch or IndeedSearch object
    :return: None - result of the task is stored in db
    because of how celery.Task is configured we don't need the app_context() here
    """
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
    all parameters of a celery task must be serializable
    :param self: celery sets this argument
    :param linkedin_credentials: fake username and password for scraping
    :param search_fields: for linkedin search

    """
    print('starting linkedin search', search_fields)
    search_fields = convert_search_fields(search_fields, 'linkedin')
    new_search = LinkedinSearch(**search_fields, linkedin_credentials=linkedin_credentials)
    # TODO it creates a new loop for each task, replace with a single loop
    result = asyncio.run(async_task(
        new_search=new_search,
        task_update_state=self.update_state
    ))
    # https://docs.celeryq.dev/en/latest/userguide/tasks.html#success
    return result


@shared_task(bind=True)
def scrape_indeed(self, search_fields: dict, linkedin_credentials: dict):
    """
    all parameters of a celery task must be serializable
    :param self: celery sets this argument
    :param linkedin_credentials: fake username and password for scraping
    :param search_fields: for linkedin search
    """
    print('starting indeed search', search_fields)
    search_fields = convert_search_fields(search_fields, 'indeed')
    new_search = IndeedSearch(**search_fields)
    # TODO it creates a new loop for each task, replace with a single loop
    result = asyncio.run(async_task(
        new_search=new_search,
        task_update_state=self.update_state
    ))
    # https://docs.celeryq.dev/en/latest/userguide/tasks.html#success
    return result


def get_task_state(task_id):
    """
    :param task_id:
    :return: {
    "state": "PROGRESS" | "BEGUN" | "REVOKED" | "SUCCESS"
    "info": {  # up to date version in BaseSearch.py
        "total": int,
        "current": int,
        "job_count": int
    }
}
    """
    task = AsyncResult(task_id)
    if task.state == 'SUCCESS':
        info = task.get()
    elif task.state == 'PROGRESS':
        info = task.info
    else:
        info = str(task.info)
    return {
        'state': task.state,
        'info': info
    }


def revoke_task(task_id):
    AsyncResult(task_id).revoke(terminate=True, signal='SIGKILL')


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
