import asyncio
import logging
from pprint import pprint
from typing import Type

from celery import shared_task
from celery.result import AsyncResult
from playwright.async_api import async_playwright
from playwright.async_api._generated import Page as PlayWrightPage
from sqlalchemy import delete

from bas_app.api.search.search_fields_reference import reference
from bas_app.models import Job, Search
from bas_app.scraper.BaseBrowserSearch import BaseBrowserSearch
from bas_app.scraper.BaseSearch import BaseSearch
from bas_app.scraper.BuiltinSearch import BuiltinSearch
from bas_app.scraper.IndeedSearch import IndeedSearch
from bas_app.scraper.LinkedinSearch import LinkedinSearch
from bas_app import db, ext_celery

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
from config import pwt_args


async def async_browser_task(
        new_search: Type[BaseBrowserSearch],
        task_update_state: callable,
):
    """
    :param new_search: LinkedinSearch or IndeedSearch object
    :task_update_state: update_state fuc from celery
    :return: None - result of the task is stored in db
    because of how celery.Task is configured we don't need the app_context() here
    """
    async with async_playwright() as pwt:
        browser = await pwt.chromium.launch_persistent_context(**pwt_args())
        bpage: PlayWrightPage = await browser.new_page()

        task_update_state(state='BEGUN')
        bpage: PlayWrightPage = await new_search.create_session(
            bpage=bpage,
            task_update_state=task_update_state)  # one session for each task
        await new_search.populate(bpage=bpage)
        meta = new_search.meta.copy()
        return meta


# def remove_job_duplicates():
#     # delete duplicate rows in db https://stackoverflow.com/a/3317575/5320906
#     # Create a query that identifies the row for each domain with the lowest id
#     inner_q = db.session.query(db.func.min(Job.id)).group_by(Job.description_text, Job.title, Job.company_id)
#     aliased = db.alias(inner_q)
#     # Select the rows that do not match the subquery
#     q = db.session.query(Job).filter(~Job.id.in_(aliased))
#     # Delete the unmatched rows (SQLAlchemy generates a single DELETE statement from this loop)
#     count_deleted = 0
#     for job in q:
#         db.session.execute(delete(Search).where(Search.job_id == job.id))
#         db.session.delete(job)
#         count_deleted += 1
#     db.session.commit()
#     return count_deleted


@shared_task(bind=True, serializer='pickle')
def scrape_linkedin(self, search_fields: dict, user_id: int,
                    search_model_id: int, credentials: dict):
    """
    all parameters of a celery task must be serializable
    :param self: celery sets this argument
    :param credentials: fake username and password for scraping
    :param search_fields: for linkedin search
    :param user_id: id of row in db table user
    :param search_model_id: id of row in db table search_model
    """
    logging.info(f'{self.request.id} starting linkedin search {search_fields}')
    search_fields = convert_search_fields(search_fields, 'linkedin')
    new_search = LinkedinSearch(**search_fields,
                                linkedin_credentials=credentials,
                                user_id=user_id,
                                search_model_id=search_model_id,
                                task_id=self.request.id)
    # TODO it creates a new loop for each task, replace with a single loop
    result = asyncio.run(async_browser_task(
        new_search=new_search,
        task_update_state=self.update_state
    ))
    # https://docs.celeryq.dev/en/latest/userguide/tasks.html#success
    return result


@shared_task(bind=True)
def scrape_indeed(self, search_fields: dict, user_id: int,
                  search_model_id: int, credentials: dict = None):
    """
    all parameters of a celery task must be serializable
    :param self: celery sets this argument
    :param search_fields: for linkedin search
    :param user_id: id of row in db table user
    :param search_model_id: id of row in db table search_model
    """
    logging.info(f'{self.request.id} starting indeed search {search_fields}')
    search_fields = convert_search_fields(search_fields, 'indeed')
    new_search = IndeedSearch(**search_fields,
                              user_id=user_id,
                              search_model_id=search_model_id,
                              task_id=self.request.id)
    # TODO it creates a new loop for each task, replace with a single loop
    result = asyncio.run(async_browser_task(
        new_search=new_search,
        task_update_state=self.update_state
    ))
    # https://docs.celeryq.dev/en/latest/userguide/tasks.html#success
    return result


@shared_task(bind=True)
def scrape_builtin(self, search_fields: dict, user_id: int,
                   search_model_id: int, credentials: dict = None):
    """
    all parameters of a celery task must be serializable
    :param self: celery sets this argument
    :param search_fields: for linkedin search
    :param user_id: id of row in db table user
    :param search_model_id: id of row in db table search_model
    """
    logging.info(f'{self.request.id} starting builtin search {search_fields}')
    new_search = BuiltinSearch(**search_fields,
                               user_id=user_id,
                               search_model_id=search_model_id,
                               task_id=self.request.id)
    result = asyncio.run(async_api_task(
        new_search=new_search,
        task_update_state=self.update_state
    ))
    # https://docs.celeryq.dev/en/latest/userguide/tasks.html#success
    return result


async def async_api_task(
        new_search: BaseSearch,
        task_update_state: callable,
):
    """
    :param new_search: BuiltinSearch object
    :param task_update_state: update func from celery
    :return: None - result of the task is stored in db
    """
    task_update_state(state='BEGUN')
    new_search.run_api(task_update_state)


def inspect_is_reserved(task_id: str):
    inspect = ext_celery.celery.control.inspect()
    # print('reserved')
    # pprint(inspect.reserved())  # have been received, but are still waiting to be executed
    workers = inspect.reserved()
    task_ids = []
    if type(workers) is list:
        task_ids = [[t.get('id') for worker in workers for t in list(worker.values())[0]]]
    else:
        worker_tasks = list(workers.values())[0]
        if len(worker_tasks):
            task_ids = [t.get('id') for t in worker_tasks]
    # print('reserved-->')
    # pprint(task_ids)
    return task_id in task_ids


def inspect_is_scheduled(task_id: str):
    inspect = ext_celery.celery.control.inspect()
    # print('scheduled')
    # pprint(inspect.scheduled())  # waiting to be scheduled
    workers = inspect.scheduled()
    task_ids = []
    if type(workers) is list:
        workers_tasks = [wt for w in workers for wt in list(w.values())[0]]
        task_ids = [wt.get('request').get('id') for wt in workers_tasks if wt.get('request')]
    else:
        worker_tasks = list(workers.values())[0]
        if len(worker_tasks):
            task_ids = [t.get('request').get('id') for t in worker_tasks]
    # print('scheduled-->')
    # pprint(task_ids)
    return task_id in task_ids


def inspect_is_active(task_id: str):
    inspect = ext_celery.celery.control.inspect()
    # print('active')
    # pprint(inspect.active())
    workers = inspect.active()
    task_ids = []
    if type(workers) is list:
        task_ids = [[t.get('id') for worker in workers for t in list(worker.values())[0]]]
    else:
        worker_tasks = list(workers.values())[0]
        if len(worker_tasks):
            task_ids = [t.get('id') for t in worker_tasks]
    # print('active-->')
    # pprint(task_ids)
    return task_id in task_ids


def get_task_state(task_id):
    """
    :param task_id:
    :return: {
    "state": "PROGRESS" | "BEGUN" | "REVOKED" | "SUCCESS | "VERIFICATION" | "PENDING" | "SENT" | "FAILURE" | "CLEARED"
    "info": {  # up-to-date version in BaseBrowserSearch.py
        "total": int,
        "current": int,
        "job_count": int,
        "task_id": str?
    }
}
    """
    # https://docs.celeryq.dev/en/latest/userguide/workers.html#inspecting-workers

    task = AsyncResult(task_id)

    if task.state == 'PENDING':
        actives = inspect_is_active(task_id)
        scheduleds = inspect_is_scheduled(task_id)
        reserveds = inspect_is_reserved(task_id)
        if not actives and not scheduleds and not reserveds:
            return {
                'state': "CLEARED"
            }

    info = str(task.info)
    if task.state == 'SUCCESS':
        info = task.get()
    if task.state == 'PROGRESS' or task.state == 'VERIFICATION' or task.state == 'VERIFYING':
        info = task.info

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

    result = {}
    for k, v in input_fields.items():
        if k in reference[job_board].keys():
            if v is None:
                v = ''  # fixes keyError: None
            if k == 'experience' and job_board == 'linkedin':
                experience = [reference[job_board][k][exp] for exp in input_fields[k]]
                result[k] = experience
            else:
                # logging.info(f"k: {k}")
                # logging.info(f"v: {v}")
                result[k] = reference[job_board][k][v]

        else:
            result[k] = v
    return result
