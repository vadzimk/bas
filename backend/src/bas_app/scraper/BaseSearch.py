import asyncio
import logging
import math
import random
import sys
from abc import ABC, abstractmethod
from typing import List, Optional

from BasePage import BasePage
from bas_app import db
from bas_app.models import Job, Company
from bas_app.scraper.BaseBeacon import BaseBeacon
from typing import Type
from playwright.async_api._generated import Page as PlayWrightPage


class FoundException(Exception):
    pass  # do nothing (only break out of the try block)


class BaseSearch(ABC):
    NAVIGATE_DELAY = 15

    def __init__(self, what, where, age, radius, experience, limit, user_id, search_model_id, task_id):
        self._query = what
        self._location = where
        self._age = age
        self._radius = radius
        self._experience = experience
        self._pages: Optional[List[BasePage]] = None
        self._PageClass = BasePage
        self._url = None
        self._pages = []
        self._limit: int = int(limit) if limit else sys.maxsize
        self._task_update_state = None
        self._task_state_meta = {
            'total': 0,  # page_count + beacon count
            'current': 0,
            'job_count': 0,
            'job_duplicates_current': 0
        }
        self._page_count_with_limit = None
        self._total_skipped = 0,
        self._user_id = user_id,
        self._search_model_id = search_model_id,
        self._task_id = task_id

    def get_navigate_delay(self):
        assert self.NAVIGATE_DELAY > 10
        return random.uniform(self.NAVIGATE_DELAY - 8, self.NAVIGATE_DELAY + 8)

    @property
    def pages(self):
        return self._pages

    @property
    def meta(self):
        return self._task_state_meta

    @abstractmethod
    async def create_session(self,
                             bpage,
                             task_update_state: callable = lambda state, meta: None
                             ):
        """
        logs into the website and returns the bpage
        :param bpage: base page
        :param task_update_state: the celery.Task.update_state() method to update task state passed from tasks
        """
        return bpage

    async def populate(self, bpage: PlayWrightPage ):
        """
        entry point to crawl job board pages
        :param bpage: instance of playwright page
        """
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

    # @staticmethod
    # def insert_or_update_job_db(beacon):
    #     """ creates or updates job record in db"""
    #     job = Job.query.filter_by(url=beacon.dict.get('url')).first()
    #     if not job:  # create record
    #         job_attributes = filter_attributes_job(beacon)
    #         job = Job(**job_attributes)
    #         db.session.add(job)
    #     else:  # update record
    #         for k, v in filter_attributes_job(beacon).items():
    #             if v:
    #                 setattr(job, k, v)
    #     db.session.commit()

    @staticmethod
    def insert_or_update_job_db(beacon: Type[BaseBeacon]):
        """ creates or updates job record in db"""
        BaseSearch.insert_or_update_relation_helper(
            Table=Job,
            fields=beacon.job_attributes_only,
            filter_column='url',
            filter_value=beacon.dict.get('url')
        )

    async def populate_details(self, bpage: PlayWrightPage):
        """ Populate job post details form 'iframe' and
        populate company details from the company profile page
        """
        for page_index, p in enumerate(self._pages):
            for b_index, b in enumerate(p.beacons):
                job_url = b.dict.get('url')  # TODO change to  b.dict['url'] and sometimes it will throw  KeyError('url')
                if not job_url:
                    logging.critical(f"url missing in {b.dict}")
                    continue
                job = Job.query.filter_by(
                    url=job_url).first()  # TODO monitor this returned none although the url was found in db, probably change to postgresdb
                # indeed creates a new unique url each time you browse, now way around duplicates
                if not (job and job.description_text):  # not (job details and company details) are already in db
                    await asyncio.sleep(self.get_navigate_delay())
                    await self.populate_job_post_details(b, job_url, bpage)
                    self.insert_or_update_job_db(b)
                try:
                    company_profile_url = b.dict['company'].get('profile_url') or (
                            job and job.company and job.company.profile_url)
                except Exception as e:
                    print("excapt")
                    raise e
                # TODO implement utils.normalize_company_homepage_url and compare with normalized url
                # TODO change schema to have linkedin_profile_url and indeed_profile_url to aggregate from company data from both platforms
                # TODO if particular profile_url_missing then update values,else skip going to profile_url
                company = company_profile_url and Company.query.filter_by(profile_url=company_profile_url).first()
                if not (company and company.homepage_url):  # not company already in db
                    # continue
                    await asyncio.sleep(self.get_navigate_delay())
                    await self.populate_company_details(b, company_profile_url, bpage)
                    company = self.insert_or_update_company_db(b)
                job.company_id = company.id
                db.session.commit()
                self._task_state_meta['current'] += 1
                self.update_state()

    @staticmethod
    def insert_or_update_relation_helper(Table: db.Model, fields: dict, filter_column: str, filter_value: str):
        """ generic insert or update relation into db
        inserts a new row or updates it if exists
        :Table: db.Model to insert fields
        :fields: fields of the row {attribute:value}
        :filter_column: where column
        :filter_value: where value
        :return: query row result
        """
        where = {filter_column: filter_value}
        existing_row = Table.query.filter_by(**where).first()
        if not existing_row:  # create record
            new_row = Table(**fields)
            db.session.add(new_row)
        else:  # update record
            for k, v in fields.items():
                if v:
                    setattr(existing_row, k, v)
        db.session.commit()
        return existing_row or new_row

    # @staticmethod
    # def insert_or_update_company_db(beacon):
    #     """ saves company fields of the beacon to db if company not present in db"""
    #     company = Company.query.filter_by(profile_url=beacon.dict['company'].get('profile_url')).first()
    #     if not company:
    #         company_attributes = beacon.dict['company']
    #         company = Company(**company_attributes)
    #         db.session.add(company)
    #     db.session.commit()
    #     return company

    @staticmethod
    def insert_or_update_company_db(beacon):
        """ saves company fields of the beacon to db if company not present in db"""
        company = BaseSearch.insert_or_update_relation_helper(
            Table=Company,
            fields=beacon.dict['company'],
            filter_column='profile_url',
            filter_value=beacon.dict['company'].get('profile_url')
        )
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
            page.save_beacons_job_db(
                user_id=self._user_id,
                search_model_id=self._search_model_id,
                task_id=self._task_id)  # this is synchronous
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
                await asyncio.sleep(self.get_navigate_delay())
                # print(f'''{self._task_state_meta['current']}/{self._task_state_meta['total']} "current"''')
                # print("-"*10)
        self._pages = pages
        return bpage
