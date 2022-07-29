import math
import time
import urllib
from enum import Enum
from typing import List
from utils import override
from IndeedPage import IndeedPage
from BaseSearch import BaseSearch


class IndeedSearch(BaseSearch):
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
                 education=Filters.Education.ALL):
        super().__init__(what, where, age, radius, experience, education)
        self._url = f"""https://www.indeed.com/jobs?q={urllib.parse.quote(self._query)}&l={urllib.parse.quote(self._location)}{self.attributes()}{self._radius}&fromage={self._age}"""
        self._PageClass = IndeedPage


    @override
    @staticmethod
    async def populate_job_post_details(beacon, job_url, bpage):
        try:
            await bpage.goto(job_url)
            text = await bpage.inner_html('html')
            beacon.populate_from_details(text)
        except Exception as e:
            print(f'Error going to {job_url}', e)

    @override
    @staticmethod
    async def populate_company_details(beacon, company_url, bpage):
        try:
            await bpage.goto(f'{company_url}')
            about_company = bpage.locator('main')
            about_company_html = await about_company.inner_html()

            beacon.populate_from_company_profile(about_company_html, None)
        except Exception as e:
            print(f'Error going to {company_url}', e)


    @override
    async def create_session(self, bpage):
        """ logs into the website and returns the bpage"""
        return bpage

    def attributes(self) -> str:
        """
        combines education and experience to pass in the query string
        :return: string of the form '&sc=0kf%3Aattr(EXSNN%7CFCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)explvl(SENIOR_LEVEL)%3B' or empty string
        """
        attributes = f'{self._education}{self._experience}'
        return f'{"&sc=0kf%3A" if attributes else ""}{attributes}{"%3B" if attributes else ""}'
