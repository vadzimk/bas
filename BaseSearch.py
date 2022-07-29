import math
import time
from abc import ABC, abstractmethod
from typing import List, Optional

from BasePage import BasePage


class FoundException(Exception):
    pass  # do nothing (only break out of the try block)


class BaseSearch(ABC):
    NAVIGATE_DELAY = 3

    def __init__(self, what, where, age, radius, experience, education=''):
        self._query = what
        self._location = where
        self._age = age
        self._radius = radius
        self._experience = experience
        self._education = education
        self._pages: Optional[List[BasePage]] = None
        self._PageClass = BasePage
        self._url = None
        self._pages = []

    @property
    def pages(self):
        return self._pages

    @abstractmethod
    async def create_session(self, bpage):
        """ logs into the website and returns the bpage"""
        return bpage

    async def populate(self, bpage):
        bpage = await self.create_session(bpage)
        bpage = await self.flip_pages(bpage)
        await self.populate_details(bpage)

    @staticmethod
    @abstractmethod
    async def populate_company_details(beacon, company_url, bpage):
        pass

    @staticmethod
    @abstractmethod
    async def populate_job_post_details(beacon, job_url, bpage):
        pass

    async def populate_details(self, bpage):
        """ Populate details form 'iframe' """
        for page_index, p in enumerate(self._pages):
            if page_index == 1: break  # TODO remove it, this is for testiong only
            for b in p.beacons:
                job_url = b.dict['url']
                await self.populate_job_post_details(b, job_url, bpage)
                time.sleep(BaseSearch.NAVIGATE_DELAY)
                company_profile_url = b.dict['company'].get('profile_url')
                company_homepage = b.dict['company'].get('homepage')
                try:
                    for page in self._pages:
                        for bec in page.beacons:
                            if company_homepage is not None and company_homepage == bec.dict['company'].get(
                                    'homepage'):  # already have this company in the source
                                self.copy_company_details(bec, b)
                                raise FoundException()
                except FoundException:
                    print(f'Found previous beacon for company {b.dict["company"].get("name")}')
                else:
                    await self.populate_company_details(b, company_profile_url, bpage)
                    time.sleep(BaseSearch.NAVIGATE_DELAY)

    def copy_company_details(self, from_bec, to_bec):
        to_bec.populate_company_from_bec(from_bec)

    async def flip_pages(self, bpage):
        async def make_page(n, url, Type):
            nonlocal pages, bpage
            # try:
            page = Type(n, url)
            await page.populate(bpage)
            pages.append(page)
            # except Exception as e:
            #     print('-' * 20)
            #     print(f'page {n} not created ', e)
            #     print('-' * 20)

        pages: List[BasePage] = []
        await make_page(0, self._url, self._PageClass)
        page_count = math.ceil(pages[0].job_count / pages[0].JOBS_ON_PAGE)
        print(page_count, 'page_count for search', self._url)
        if page_count > 1:
            for page_n in range(1, page_count):
                await make_page(1, self._url, self._PageClass)
                time.sleep(BaseSearch.NAVIGATE_DELAY)
                if page_n == 1:
                    break  # TODO remove this line, it is to limit pages for test
        self._pages = pages
        return bpage
