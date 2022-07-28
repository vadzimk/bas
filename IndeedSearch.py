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

    @override
    async def populate(self, bpage):
        self._pages = await self.flip_pages(bpage)
        await self.populate_details(bpage)

    async def populate_details(self, bpage):
        """ Populate details form 'iframe' """
        for page_index, p in enumerate(self._pages):
            if page_index == 1: break  # TODO remove it, this is for testiong only
            for b in p.beacons:
                job_url = b.dict['url']
                await self.populate_job_post_details(b, job_url, bpage)
                time.sleep(3)
                company_url = b.dict.get('company_profile_url')
                await self.populate_company_details(b, company_url, bpage)
                time.sleep(3)

    @staticmethod
    async def populate_job_post_details(beacon, job_url, bpage):
        try:
            await bpage.goto(job_url)
            text = await bpage.inner_html('html')
            beacon.populate_from_details(text)
        except Exception as e:
            print(f'Error going to {job_url}', e)

    @staticmethod
    async def populate_company_details(beacon, company_url, bpage):
        # TODO add populate_from_company_profile
        pass

    @override
    async def flip_pages(self, bpage):
        async def make_page(n, url):
            nonlocal pages, bpage
            try:
                page = IndeedPage(n, url)
                await page.populate(bpage)
                pages.append(page)
            except Exception as e:
                print('-' * 20)
                print(f'page {n} not created ', e)
                print('-' * 20)

        pages: List[IndeedPage] = []
        # page0 = IndeedPage(0, self._url)
        # pages.append(page0)
        await make_page(0, self._url)
        page_count = math.ceil(pages[0].job_count / pages[0].JOBS_ON_PAGE) if len(pages) >= 1 else 0
        print(page_count, ' page_count for search ', self._url)
        if page_count > 1:
            for page_n in range(1, page_count + 1):
                await make_page(page_n, self._url)
        return pages

    def attributes(self) -> str:
        """
        combines education and experience to pass in the query string
        :return: string of the form '&sc=0kf%3Aattr(EXSNN%7CFCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)explvl(SENIOR_LEVEL)%3B' or empty string
        """
        attributes = f'{self._education}{self._experience}'
        return f'{"&sc=0kf%3A" if attributes else ""}{attributes}{"%3B" if attributes else ""}'
