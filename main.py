import asyncio
import time
from pprint import pprint
from typing import List, Optional

import pandas as pd

from BaseSearch import BaseSearch
from IndeedSearch import IndeedSearch
from LinkedinSearch import LinkedinSearch
from utils import cleanup, create_project
from playwright.async_api import async_playwright

indeed_searches = [
    {
        'what': "react frontend developer",
        'where': "Los Angeles",
        'age': IndeedSearch.Filters.Age.ONE,
        'radius': IndeedSearch.Filters.Radius.EXACT,
        'experience': IndeedSearch.Filters.Experience.MID}
]

linkedin_searches = [
    {
        'what': """react AND (python OR node) AND NOT (ruby OR ".NET") developer AND NOT (citizen OR Citizen OR "green card" OR "Green Card") and NOT (senior OR Senior OR lead OR Lead) AND NOT ("CyberCoders" OR "Jobot")""",
        'where': "Los Angeles, California, United States",
        'age': LinkedinSearch.Filters.Age.PAST_24H,
        'radius': LinkedinSearch.Filters.Radius.EXACT,
        'experience': [LinkedinSearch.Filters.Experience.INTERNSHIP]}
]


def mk_searches(searches: dict, Type: BaseSearch) -> List[BaseSearch]:
    return [Type(**s) for s in searches]


async def do_search(searches: List[BaseSearch]):
    job_list = []
    async with async_playwright() as pwt:
        browser = await pwt.chromium.launch(args=[''],
                                            headless=False,
                                            slow_mo=50
                                            )
        bpage = await browser.new_page()
        for one_search in searches:
            await one_search.populate(bpage)
            time.sleep(1)
            for page in one_search.pages:
                for beacon in page.beacons:
                    job_list.append(beacon.dict)
    return job_list


async def blocking():
    time.sleep(1)
    return [{'one': 1, 'two': 2}]


async def start_all(indeed_searches, linkedin_searches):
    # indeed_task = asyncio.create_task(do_search(mk_searches(indeed_searches, IndeedSearch)))
    linkedin_task = asyncio.create_task(do_search(mk_searches(linkedin_searches, LinkedinSearch)))
    res = await asyncio.gather(
        # indeed_task,
        linkedin_task)
    return [val for sub in res for val in sub]  # flatten list of lists


def main():
    job_list = asyncio.run(start_all(indeed_searches, linkedin_searches))
    df = pd.DataFrame(job_list)
    print(df)
    df.sort_values(['description_text', 'url'], ascending=[True, True], inplace=True)
    n_rows_before = len(df.index)
    df.drop_duplicates(subset=['title', 'company_name', 'description_text'], keep='first', inplace=True)
    n_rows_after = len(df.index)
    print(f'Dropped {n_rows_before - n_rows_after} duplicate rows')
    df.fillna('', inplace=True)  # fill None with ''
    # TODO uncomment this
    # # reorder the view
    # df = df[
    #     ['company_rating', 'company_name', 'multiple_candidates', 'date_posted', 'title', 'company_location', 'salary',
    #      'estimated_salary', 'job_type', 'qualifications', 'description_text', 'benefits', 'hiring_insights',
    #      'company_indeed_profile_url', 'url']]
    df.sort_values(['company_rating', 'company_name', 'title'], ascending=[False, True, True], inplace=True)

    df.to_csv('out/search.csv')
    df.to_pickle('out/dataframe.pickle')


if __name__ == '__main__':
    cleanup()
    create_project()
    main()

#  get first page
#  get number of pages div id=searchCountPages
#  get links to the jobs
#  parse each link
#  get job attributes
# >  break apart full job description
#  find red flags
#  find good flags
