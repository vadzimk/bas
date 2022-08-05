import asyncio
from typing import List

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
        'experience': IndeedSearch.Filters.Experience.ALL
    },
    {
        'what': "flask python developer",
        'where': "Los Angeles",
        'age': IndeedSearch.Filters.Age.SEVEN,
        'radius': IndeedSearch.Filters.Radius.ALL,
        'experience': IndeedSearch.Filters.Experience.ALL
    },
    {
        'what': "javascript developer",
        'where': "Los Angeles",
        'age': IndeedSearch.Filters.Age.SEVEN,
        'radius': IndeedSearch.Filters.Radius.ALL,
        'experience': IndeedSearch.Filters.Experience.ALL
    },
]

linkedin_searches = [
    {
        'what': f"""react AND (python OR node) developer {os.getenv('LINKEDIN_BASE_SEARCH')}""",
        'where': "Los Angeles, California, United States",
        'age': LinkedinSearch.Filters.Age.PAST_WEEK,
        'radius': LinkedinSearch.Filters.Radius.ALL,
        'experience': [
            LinkedinSearch.Filters.Experience.INTERNSHIP,
            LinkedinSearch.Filters.Experience.ENTRY_LEVEL,
            LinkedinSearch.Filters.Experience.MID_SENIOR,
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
            for one_search in searches:
                await one_search.populate(bpage)
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


# async def blocking():
#     await asyncio.sleep(1)
#     return [{'one': 1, 'two': 2}]


async def start_all(indeed_searches, linkedin_searches):
    indeed_task = asyncio.create_task(do_search(mk_searches(indeed_searches, IndeedSearch)))
    linkedin_task = asyncio.create_task(do_search(mk_searches(linkedin_searches, LinkedinSearch)))

    done, pending = await asyncio.wait([indeed_task, linkedin_task], return_when=asyncio.FIRST_EXCEPTION)
    # print(f'done tasks count {len(done)}')
    # print(f'pending tasks count {len(pending)}')

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

    df.to_csv('out/search.csv')
    df.to_pickle('dataframe.pickle')


if __name__ == '__main__':
    cleanup()
    create_project()
    main()
