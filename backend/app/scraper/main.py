import asyncio
import logging
from typing import List

from BaseSearch import BaseSearch
from IndeedSearch import IndeedSearch
from LinkedinSearch import LinkedinSearch
from utils import cleanup, create_project
from playwright.async_api import async_playwright

from backend.app import create_app, db
from backend.app.models import Job
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')  # access  flask-sqlalchemy
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/


indeed_searches = [
    # {
    #     'what': "react frontend developer",
    #     'where': "Los Angeles",
    #     'age': IndeedSearch.Filters.Age.SEVEN,
    #     'radius': IndeedSearch.Filters.Radius.ALL,
    #     'experience': IndeedSearch.Filters.Experience.ALL
    # },
    # {
    #     'what': "python developer",
    #     'where': "Los Angeles",
    #     'age': IndeedSearch.Filters.Age.SEVEN,
    #     'radius': IndeedSearch.Filters.Radius.ALL,
    #     'experience': IndeedSearch.Filters.Experience.ALL
    # },
    # {
    #     'what': "javascript developer",
    #     'where': "Los Angeles",
    #     'age': IndeedSearch.Filters.Age.SEVEN,
    #     'radius': IndeedSearch.Filters.Radius.ALL,
    #     'experience': IndeedSearch.Filters.Experience.ALL
    # },
    # {
    #     'what': "software automation engineer",
    #     'where': "Los Angeles",
    #     'age': IndeedSearch.Filters.Age.SEVEN,
    #     'radius': IndeedSearch.Filters.Radius.ALL,
    #     'experience': IndeedSearch.Filters.Experience.ENTRY
    # },
    {
        'what': "software automation tester",
        'where': "Los Angeles",
        'age': IndeedSearch.Filters.Age.SEVEN,
        'radius': IndeedSearch.Filters.Radius.ALL,
        'experience': IndeedSearch.Filters.Experience.ENTRY
    },
]

linkedin_searches = [
    # {
    #     'what': f"""react frontend developer {os.getenv('LINKEDIN_BASE_SEARCH')}""",
    #     'where': "Los Angeles, California, United States",
    #     'age': LinkedinSearch.Filters.Age.ALL,
    #     'radius': LinkedinSearch.Filters.Radius.ALL,
    #     'experience': [
    #         LinkedinSearch.Filters.Experience.INTERNSHIP,
    #         LinkedinSearch.Filters.Experience.ENTRY_LEVEL,
    #         LinkedinSearch.Filters.Experience.MID_SENIOR,
    #     ]
    # },
    # {
    #     'what': f"""python developer {os.getenv('LINKEDIN_BASE_SEARCH')}""",
    #     'where': "Los Angeles, California, United States",
    #     'age': LinkedinSearch.Filters.Age.ALL,
    #     'radius': LinkedinSearch.Filters.Radius.ALL,
    #     'experience': [
    #         LinkedinSearch.Filters.Experience.INTERNSHIP,
    #         LinkedinSearch.Filters.Experience.ENTRY_LEVEL,
    #         LinkedinSearch.Filters.Experience.MID_SENIOR,
    #     ]
    # },
    # {
    #     'what': f"""javascript developer {os.getenv('LINKEDIN_BASE_SEARCH')}""",
    #     'where': "Los Angeles, California, United States",
    #     'age': LinkedinSearch.Filters.Age.ALL,
    #     'radius': LinkedinSearch.Filters.Radius.ALL,
    #     'experience': [
    #         LinkedinSearch.Filters.Experience.INTERNSHIP,
    #         LinkedinSearch.Filters.Experience.ENTRY_LEVEL,
    #         LinkedinSearch.Filters.Experience.MID_SENIOR,
    #     ]
    # },
    {
        'what': f"""software automated test {os.getenv('LINKEDIN_BASE_SEARCH')}""",
        'where': "Los Angeles, California, United States",
        'age': LinkedinSearch.Filters.Age.ALL,
        'radius': LinkedinSearch.Filters.Radius.ALL,
        'experience': [
            LinkedinSearch.Filters.Experience.ENTRY_LEVEL,
        ]
    },
]


def mk_searches(searches: dict, Type: BaseSearch) -> List[BaseSearch]:
    return [Type(**s) for s in searches]


async def do_search(searches: List[BaseSearch]):
    """
    :param searches:
    :return: None - result of the task now does not contain data, it is stored in db
    """
    async with async_playwright() as pwt:
        browser = await pwt.chromium.launch(args=[''],
                                            # headless=False,
                                            # slow_mo=50
                                            )
        bpage = await browser.new_page()
        with app.app_context():
            first_pass = True
            for one_search in searches:
                if first_pass:
                    bpage = await one_search.create_session(bpage)  # one session for each task
                await one_search.populate(bpage)
                await asyncio.sleep(1)
                first_pass = False

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


# async def blocking():
#     await asyncio.sleep(1)
#     return [{'one': 1, 'two': 2}]


async def start_all(indeed_searches, linkedin_searches):
    indeed_task = asyncio.create_task(do_search(mk_searches(indeed_searches, IndeedSearch)))
    linkedin_task = asyncio.create_task(do_search(mk_searches(linkedin_searches, LinkedinSearch)))

    done, pending = await asyncio.wait([indeed_task, linkedin_task], return_when=asyncio.FIRST_EXCEPTION)
    # print(f'done tasks count {len(done)}')
    # print(f'pending tasks count {len(pending)}')

    for i, done_task in enumerate(done):
        if done_task.exception() is None:
            logging.info(f'done task {i}')
        else:
            logging.error(f"Task got an exception: {done_task.exception()}")

    for pending_task in pending:
        pending_task.cancel()


def main():
    asyncio.run(start_all(indeed_searches, linkedin_searches), debug=True)






if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cleanup()
    create_project()
    main()
