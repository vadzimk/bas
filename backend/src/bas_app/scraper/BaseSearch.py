import asyncio
import logging
import math
import sys
from abc import ABC, abstractmethod
from typing import List, Optional

from BasePage import BasePage
from bas_app import db
from bas_app.models import Job, Company
from bas_app.scraper.utils import filter_attributes_job
from typing import Type
from playwright.async_api._generated import Page as PlayWrightPage


class FoundException(Exception):
    pass  # do nothing (only break out of the try block)


class BaseSearch(ABC):
    NAVIGATE_DELAY = 3

    def __init__(self, what, where, age, radius, experience, limit, education=''):
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
        self._limit: int = int(limit) if limit else sys.maxsize
        self._task_update_state = None
        self._task_state_meta = {
            'total': 0, # page_count + beacon count
            'current': 0,
            'job_count': 0,
            'job_duplicates_current': 0

        }
        self._page_count_with_limit = None
        self._total_skipped = 0

    @property
    def pages(self):
        return self._pages

    @property
    def meta(self):
        return self._task_state_meta

    @abstractmethod
    async def create_session(self, bpage):
        """ logs into the website and returns the bpage"""
        return bpage

    async def populate(self, bpage: PlayWrightPage, task_update_state: callable = lambda state, meta: None):
        """
        entry point to crawl job board pages
        :param bpage: instance of playwright page
        :param task_update_state: the celery.Task.update_state() method to update task state passed from tasks
        """
        self._task_update_state = task_update_state
        # TODO click on "request a new confirmation link" of found
        bpage: PlayWrightPage = await self.flip_pages(bpage)
        await self.populate_details(bpage)

    def update_state(self):
        self._task_update_state(state='PROGRESS', meta=self._task_state_meta)

    @staticmethod
    @abstractmethod
    async def populate_company_details(beacon, company_url, bpage: PlayWrightPage):
        pass

    @staticmethod
    @abstractmethod
    async def populate_job_post_details(beacon, job_url, bpage: PlayWrightPage):
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
                if v:
                    setattr(job, k, v)
        db.session.commit()

    async def populate_details(self, bpage: PlayWrightPage):
        """ Populate job post details form 'iframe' and
        populate company details from the company profile page
        """
        print("*"*15)
        job_count = 0
        for p in self._pages:
            job_count += len(p.beacons)
        print(job_count, "job_count for all pages")
        print("*"*15)

        for page_index, p in enumerate(self._pages):
            for b_index, b in enumerate(p.beacons):
                job_url = b.dict['url']
                job = Job.query.filter_by(url=job_url).first() # TODO monitor this returned none although the url was found in db, probably change to postgresdb
                if not job:
                    logging.warning(f'no job in db for {b.dict}')
                if job and job.description_text:  # job details and company details are already in db
                    self._total_skipped +=1
                    self._task_state_meta['current'] += 1
                    self._task_state_meta['job_duplicates_current'] += 1
                    self.update_state()
                    continue
                await self.populate_job_post_details(b, job_url, bpage)
                self.create_or_update_job_db(b)
                await asyncio.sleep(BaseSearch.NAVIGATE_DELAY)
                company_profile_url = b.dict['company'].get('profile_url')
                company_homepage_url = b.dict['company'].get('homepage_url')
                company = Company.query.filter_by(homepage_url=b.dict['company'].get('profile_url')).first()
                if company:  # company already in db
                    continue
                await self.populate_company_details(b, company_profile_url, bpage)
                created_company = self.save_beacon_company_db(b)
                job.company_id = created_company.id  # TODO and it throws error here AttributeError: 'NoneType' object has no attribute 'company_id'
                db.session.commit()
                self._task_state_meta['current'] += 1
                self.update_state()
                await asyncio.sleep(BaseSearch.NAVIGATE_DELAY)
                print(self._page_count_with_limit, "_page_count_with_limit")
                print(page_index, "page_index")
                print(p.JOBS_ON_PAGE, "JOBS_ON_PAGE")
                print(b_index + 1, "b_index + 1")
                print(f'''{self._task_state_meta['current']}/{self._task_state_meta['total']} "current"''')
                print(self._total_skipped, "total_skipped")
                print("-"*10)
        print(f'''{self._task_state_meta['current']}/{self._task_state_meta['total']} "current"''')
        print(self._total_skipped, "total_skipped")


    @staticmethod
    def save_beacon_company_db(beacon):
        """ saves company attributes of the beacon to db if company not present in db"""
        company = Company.query.filter_by(profile_url=beacon.dict['company'].get('profile_url')).first()
        if not company:
            company_attributes = beacon.dict['company']
            company = Company(**company_attributes)
            db.session.add(company)
        db.session.commit()
        return company

    def copy_company_details(self, from_bec, to_bec):
        to_bec.populate_company_from_bec(from_bec)

    async def flip_pages(self, bpage: PlayWrightPage) -> PlayWrightPage:
        """ navigates to successive pages of the job search results """

        async def make_page(n: int, url: str, T: Type[BasePage]):
            """ instantiates appropriate page class
            and calls populate page which creates beacon list of appropriate Beacon class
             :param n: page number
             :param url: the url for the page
             :param T: the page type to instantiate
             """
            nonlocal pages, bpage
            page: BasePage = T(n, url)
            try:
                await page.populate(bpage)
            except Exception:
                logging.critical(f'Retrying once to go to url {self._url}')
                await asyncio.sleep(1)
                await page.populate(bpage)
            page.save_beacons_job_db()  # this is synchronous
            pages.append(page)

        pages: List[BasePage] = []
        await make_page(0, self._url, self._PageClass)
        page_count = math.ceil(pages[0].job_count / pages[0].JOBS_ON_PAGE)
        self._page_count_with_limit = min(page_count, self._limit)
        job_count_with_limit = min(pages[0].job_count, self._page_count_with_limit * pages[0].JOBS_ON_PAGE)
        logging.info(f'{page_count} page_count for search {self._url}')
        self._task_state_meta['total'] = job_count_with_limit + self._page_count_with_limit
        self._task_state_meta['current'] += 1
        self._task_state_meta['job_count'] = pages[0].job_count
        self.update_state()
        if page_count > 1:
            for page_n in range(1, self._page_count_with_limit):
                await make_page(1, self._url, self._PageClass)
                self._task_state_meta['current'] += 1
                self.update_state()
                await asyncio.sleep(BaseSearch.NAVIGATE_DELAY)
                print(f'''{self._task_state_meta['current']}/{self._task_state_meta['total']} "current"''')
                print("-"*10)
        self._pages = pages
        return bpage
