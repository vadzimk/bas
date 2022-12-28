import asyncio
import logging
import math
import sys
import time
import urllib
from enum import Enum
from typing import List
from utils import override, PageCrashed
from IndeedPage import IndeedPage
from BaseBrowserSearch import BaseBrowserSearch


class IndeedSearch(BaseBrowserSearch):
    class Filters:
        class Radius(str, Enum):
            EXACT = '&radius=0'
            FIVE = '&radius=5'
            TEN = '&radius=10'
            FIFTEEN = '&radius=15'
            TWENTY_FIVE = '&radius=25'
            HUNDRED = '&radius=100'
            ALL = ''

        class Experience(str, Enum):
            ENTRY = 'explvl(ENTRY_LEVEL)'
            MID = 'explvl(MID_LEVEL)'
            SENIOR = 'explvl(SENIOR_LEVEL)'
            ALL = ''

        class Education(str, Enum):
            SCHOOL = 'attr(FCGTU%7CQJZM9%252COR)',
            ASSOCIATES = 'attr(FCGTU%7CQJZM9%7CUTPWG%252COR)',
            BACHELORS = 'attr(FCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)',
            MASTERS = 'attr(EXSNN%7CFCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)',
            ALL = ''

        class Age(str, Enum):
            LAST = 'last'
            ONE = '1'
            TREE = '3'
            SEVEN = '7'
            FOURTEEN = '14'
            ALL = ''

    def __init__(self, *,
                 what,
                 where,
                 age=Filters.Age.ALL,
                 radius=Filters.Radius.ALL,
                 experience=Filters.Experience.ALL,
                 education=Filters.Education.ALL,
                 limit: int = sys.maxsize,
                 user_id: int = None,
                 search_model_id: int = None,
                 task_id: str = None,
                 ):
        super().__init__(what=what, where=where, age=age, radius=radius, experience=experience, limit=limit,
                         user_id=user_id, search_model_id=search_model_id, task_id=task_id)

        self._education = education or ''
        self._url = f"""https://www.indeed.com/jobs?q={urllib.parse.quote(self._query)}&l={urllib.parse.quote(self._location)}{self.attributes()}{self._radius}&fromage={self._age}"""
        self._PageClass = IndeedPage

    @override
    @staticmethod
    async def populate_job_post_details(beacon, job_url, bpage):
        """ goes to the job post url and populates beacon from its html"""
        try:
            await bpage.goto(job_url)
            await asyncio.sleep(1)
            text = await bpage.inner_html('html')
            beacon.populate_from_details(text)
        except Exception as e:
            logging.error(f'Error going to {job_url}', e)
            if "Navigation failed because page crashed!" in str(e):
                raise PageCrashed(str(e))

    @override
    @staticmethod
    async def populate_company_details(beacon, company_url, bpage):
        try:
            await bpage.goto(f'{company_url}')
            about_company = bpage.locator('main')
            about_company_html = await about_company.inner_html()

            beacon.populate_from_company_profile(about_company_html, None)
        except Exception as e:
            logging.error(f'Error going to {company_url} {e}')
            if "Navigation failed because page crashed!" in str(e):
                raise PageCrashed(str(e))

    @override
    async def create_session(self,
                             bpage,
                             task_update_state: callable = lambda state, meta: None):
        """ logs into the website and returns the bpage"""
        self._task_update_state = task_update_state
        return bpage

    def attributes(self) -> str:
        """
        combines education and experience to pass in the query string
        :return: string of the form '&sc=0kf%3Aattr(EXSNN%7CFCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)explvl(SENIOR_LEVEL)%3B' or empty string
        """
        attributes = f'{self._education}{self._experience}'
        return f'{"&sc=0kf%3A" if attributes else ""}{attributes}{"%3B" if attributes else ""}'

    @override
    def run_api(self, task_update_state):
        # not applicable
        raise NotImplementedError
