import asyncio
import math
import time
from abc import ABC, abstractmethod
from typing import List, Optional

from BasePage import BasePage
from app import db
from app.models import Job, Company
from app.scraper.utils import filter_attributes_job


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

    @staticmethod
    def create_or_update_job_db(beacon):
        """ creates or updates job record in db"""
        job = Job.query.filter_by(url=beacon.dict.get('url')).first()
        if not job:  # create record
            job_attributes = filter_attributes_job(beacon)
            job = Job(**job_attributes)
            db.session.add(job)
        else:  # update record
            for k, v in filter_attributes_job(beacon).items():
                setattr(job, k, v)
        db.session.commit()

    async def populate_details(self, bpage):
        """ Populate job post details form 'iframe' and
        populate company details from the company profile page
        """
        for page_index, p in enumerate(self._pages):
            for b in p.beacons:
                job_url = b.dict['url']
                job = Job.query.filter_by(url=b.dict.get('url')).first()
                if job.description_text: # job details and company details are already in db
                    continue
                await self.populate_job_post_details(b, job_url, bpage)
                self.create_or_update_job_db(b)
                await asyncio.sleep(BaseSearch.NAVIGATE_DELAY)
                company_profile_url = b.dict['company'].get('profile_url')
                company_homepage_url = b.dict['company'].get('homepage_url')
                company = Company.query.filter_by(homepage_url=b.dict['company'].get('homepage_url')).first()
                if company: # company already in db
                    continue
                # try:
                #     for page in self._pages:
                #         for bec in page.beacons:
                #             if company_homepage_url is not None and company_homepage_url == bec.dict['company'].get(
                #                     'homepage_url'):  # already have this company in the source
                #                 self.copy_company_details(bec, b)
                #                 raise FoundException()
                # except FoundException:
                #     print(f'Found previous beacon for company {b.dict["company"].get("name")}')
                # else:
                await self.populate_company_details(b, company_profile_url, bpage)
                self.save_beacon_company_db(b)
                await asyncio.sleep(BaseSearch.NAVIGATE_DELAY)

    @staticmethod
    def save_beacon_company_db(beacon):
        """ saves company attributes of the beacon to db if company not present in db"""
        company = Company.query.filter_by(profile_url=beacon.dict['company'].get('profile_url')).first()
        if not company:
            company_attributes = beacon.dict['company']
            company = Company(**company_attributes)
            db.session.add(company)
        db.session.commit()

    def copy_company_details(self, from_bec, to_bec):
        to_bec.populate_company_from_bec(from_bec)

    async def flip_pages(self, bpage):
        """ navigates to successive pages of the job search results """

        async def make_page(n, url, Type):
            """ instantiates appropriate page class
            and calls populate page which creates beacon list of appropriate Beacon class """
            nonlocal pages, bpage
            # try:
            page: BasePage = Type(n, url)
            await page.populate(bpage)
            page.save_beacons_job_db()  # this is synchronous
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
                await asyncio.sleep(BaseSearch.NAVIGATE_DELAY)
        self._pages = pages
        return bpage
