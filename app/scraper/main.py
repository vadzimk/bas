import asyncio
import logging
import time
from pprint import pprint
from typing import List, Optional

import pandas as pd

from BaseSearch import BaseSearch
from IndeedSearch import IndeedSearch
from LinkedinSearch import LinkedinSearch
from utils import cleanup, create_project
from playwright.async_api import async_playwright

from app import create_app, db
from app.models import Job, Company
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')  # access  flask-sqlalchemy
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/


indeed_searches = [
    {
        'what': "react frontend developer",
        'where': "Los Angeles",
        'age': IndeedSearch.Filters.Age.SEVEN,
        'radius': IndeedSearch.Filters.Radius.ALL,
        'experience': IndeedSearch.Filters.Experience.ENTRY
    },
    # {
    #     'what': "flask python developer",
    #     'where': "Los Angeles",
    #     'age': IndeedSearch.Filters.Age.SEVEN,
    #     'radius': IndeedSearch.Filters.Radius.ALL,
    #     'experience': IndeedSearch.Filters.Experience.MID
    # },
    # {
    #     'what': "javascript developer",
    #     'where': "Los Angeles",
    #     'age': IndeedSearch.Filters.Age.SEVEN,
    #     'radius': IndeedSearch.Filters.Radius.ALL,
    #     'experience': IndeedSearch.Filters.Experience.MID
    # },
]

linkedin_searches = [
    # {
    #     'what': """react AND (python OR node) AND NOT (ruby OR ".NET") developer AND NOT (citizen OR Citizen OR "green card" OR "Green Card") and NOT (senior OR Senior OR lead OR Lead) AND NOT ("CyberCoders" OR "Jobot")""",
    #     'where': "Los Angeles, California, United States",
    #     'age': LinkedinSearch.Filters.Age.PAST_WEEK,
    #     'radius': LinkedinSearch.Filters.Radius.ALL,
    #     'experience': [
    #         LinkedinSearch.Filters.Experience.INTERNSHIP,
    #         LinkedinSearch.Filters.Experience.ENTRY_LEVEL,
    #         LinkedinSearch.Filters.Experience.MID_SENIOR,
    #     ]
    # },
]


def mk_searches(searches: dict, Type: BaseSearch) -> List[BaseSearch]:
    return [Type(**s) for s in searches]


async def do_search(searches: List[BaseSearch]):
    job_list = []
    async with async_playwright() as pwt:
        browser = await pwt.chromium.launch(args=[''],
                                            # headless=False,
                                            # slow_mo=50
                                            )
        bpage = await browser.new_page()
        with app.app_context():
            for one_search in searches:
                await one_search.populate(bpage)
                await asyncio.sleep(1)
                # TODO the job_list now does not contain data, it is stored in db
                # for page in one_search.pages:
                #     for beacon in page.beacons:
                #         job_list.append(beacon.dict)

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

    # TODO the job_list now does not contain data, it is stored in db
    return job_list


# async def blocking():
#     await asyncio.sleep(1)
#     return [{'one': 1, 'two': 2}]


async def start_all(indeed_searches, linkedin_searches):
    indeed_task = asyncio.create_task(do_search(mk_searches(indeed_searches, IndeedSearch)))
    linkedin_task = asyncio.create_task(do_search(mk_searches(linkedin_searches, LinkedinSearch)))

    # Changing this to handle exceptions in the running tasks
    # res = await asyncio.gather(
    #     indeed_task,
    #     linkedin_task)

    done, pending = await asyncio.wait([indeed_task, linkedin_task], return_when=asyncio.FIRST_EXCEPTION)
    # print(f'done tasks count {len(done)}')
    # print(f'pending tasks count {len(pending)}')

# TODO, remove this, this is replaced by database
    # res = []  # task results
    # for done_task in done:
    #     if done_task.exception() is None:
    #         res.append(done_task.result())
    #     else:
    #         logging.error('Error in task ', exc_info=done_task.exception())
    #         # if isinstance(done_task.exception(), TaskError ):
    #         #     pass
    # for pending_task in pending:
    #     pending_task.cancel()
    # return [val for sub in res for val in sub]  # flatten list of lists

    with app.app_context():
        result = db.session.query(Company, Job).join(Company).all()
        res = []
        for c, j in result:
            j_dict = j.__dict__
            j_dict.pop('_sa_instance_state', None)

            c_dict = c.__dict__
            c_dict.pop('_sa_instance_state', None)

            res.append({**j_dict, **c_dict})
        return res


def main():
    job_list = asyncio.run(start_all(indeed_searches, linkedin_searches), debug=True)
    if not job_list:
        exit(1)
    df = pd.json_normalize(job_list, sep='_')
    print(df)
    df.fillna('', inplace=True)
    # df.sort_values(['description_text', 'url'], ascending=[True, True], inplace=True)
    # n_rows_before = len(df.index)
    # df.drop_duplicates(subset=['title', 'company_name', 'description_text'], keep='first', inplace=True)
    # n_rows_after = len(df.index)
    # print(f'Dropped {n_rows_before - n_rows_after} duplicate rows')

    # reorder the view
    df.sort_values(['rating', 'name', 'title'], ascending=[False, True, True], inplace=True)
    columns = [
        'id',
        'title',
        'job_type',
        'qualifications',
        'salary',
        'estimated_salary',
        'date_posted',
        'multiple_candidates',
        'benefits',
        'description_markdown',
        'description_text',
        'description_html',
        'hiring_insights',
        'name',
        'rating',
        'industry',
        'size',
        'overview',
        'number_employees',
        'location',
        'main_country_name',
        'main_country_number_employees',
        'other_locations_employees',
        'other_locations_employees_html',
        'profile_url',
        'homepage_url',
        'url',
    ]
    df = df.reindex(columns=columns)

    # make id column TODO  this is not needed bc id comes from db
    # df = df.reset_index(drop=True)
    # df.index.name = 'id'
    # df.reset_index(inplace=True)

    df.to_csv('out/search.csv')
    df.to_pickle('dataframe.pickle')


if __name__ == '__main__':
    cleanup()
    create_project()
    main()
