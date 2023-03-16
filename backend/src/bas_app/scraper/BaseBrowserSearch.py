import asyncio
import logging
import math
import random
import sys
import time
from abc import ABC, abstractmethod
from pprint import pprint
from typing import List, Optional

from BasePage import BasePage
from bas_app import db
from bas_app.models import Job, Company
from typing import Type
from playwright.async_api._generated import Page as PlayWrightPage

from bas_app.scraper.BaseSearch import BaseSearch


class FoundException(Exception):
    pass  # do nothing (only break out of the try block)


class BaseBrowserSearch(BaseSearch, ABC):
    NAVIGATE_DELAY = 15

    def __init__(self, what, where, age, radius, experience, limit, user_id, search_model_id, task_id):
        super().__init__(user_id=user_id, search_model_id=search_model_id, task_id=task_id)
        self._query = what
        self._location = where
        self._age = age
        self._radius = radius
        self._experience = experience
        self._PageClass = BasePage
        self._url = None
        self._limit: int = int(limit) if limit else sys.maxsize


    def get_navigate_delay(self):
        assert self.NAVIGATE_DELAY > 10
        return random.uniform(self.NAVIGATE_DELAY - 8, self.NAVIGATE_DELAY + 8)


    @abstractmethod
    async def create_session(self,
                             bpage,
                             task_update_state: callable = lambda state, meta: None
                             ):
        """
        logs into the website and returns the playwright_page
        :param bpage: base page
        :param task_update_state: the celery.Task.update_state() method to update task state passed from tasks
        """
        return bpage

    async def populate(self, bpage: PlayWrightPage ):
        """
        entry point to crawl job board pages
        :param bpage: instance of playwright page
        """
        await self.flip_pages(bpage)
        # await self.populate_details(bpage) was put inside the flip_pages
        # such that populate happens after each pagination page was crawled
        # instead of crawling pagination exhaustively first

    @staticmethod
    @abstractmethod
    async def populate_company_details(beacon, company_profile_url, bpage: PlayWrightPage):
        pass

    @staticmethod
    @abstractmethod
    async def populate_job_post_details(beacon, job_url, bpage: PlayWrightPage):
        pass

    async def populate_details(self, playwright_page: PlayWrightPage, pagination_page: BasePage):
        """ Populate job post details form 'iframe' and
        populate company details from the company profile page
        """
        for b_index, b in enumerate(pagination_page.beacons):
            job_url = b.dict.get('url')
            if not job_url:
                logging.critical(f"url missing in {b.dict}")
                continue
            job = Job.query.filter_by(
                url=job_url).first()  # TODO monitor this returned none although the url was found in db
            # indeed creates a new unique url each time you browse, now way around duplicates
            if not (job and job.description_text):  # not (job details and company details) are already in db
                await asyncio.sleep(self.get_navigate_delay())
                await self.populate_job_post_details(b, job_url, playwright_page)
                job = self.insert_or_update_job_db(b)
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
                await self.populate_company_details(b, company_profile_url, playwright_page)
                if not b.dict.get('company').get('profile_url'):  # patches missing profile_url such that a new row w/o profile_url is not added by the insert_or_update_company_db
                    b.dict['company']['profile_url'] = company_profile_url
                company = self.insert_or_update_company_db(b)
                logging.info(f'insert or update company: {company}')
            job.company_id = company.id
            db.session.commit()
            count_deleted = BaseSearch.remove_job_duplicates()
            self._task_state_meta['job_duplicates_current'] += count_deleted
            self._task_state_meta['current'] += 1
            self.update_state()


    def copy_company_details(self, from_bec, to_bec):
        to_bec.populate_company_from_bec(from_bec)

    async def flip_pages(self, bpage: PlayWrightPage) -> PlayWrightPage:
        """ navigates to successive pagination pages of the job search results
        and populates them with details in-between"""

        async def make_page(n: int, url: str, T: Type[BasePage]):
            """ instantiates appropriate page class
            and calls populate page which creates beacon list of appropriate Beacon class
             :param n: page number
             :param url: the url for the page
             :param T: the page type to instantiate
             """
            nonlocal bpage
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
            return page

        page_0 = await make_page(0, self._url, self._PageClass)
        page_count = math.ceil(page_0.job_count / page_0.JOBS_ON_PAGE)
        self._page_count_with_limit = min(page_count, self._limit)
        job_count_with_limit = min(page_0.job_count, self._page_count_with_limit * page_0.JOBS_ON_PAGE)
        logging.info(f'{page_count} page_count for search {self._url}')
        self._task_state_meta['total'] = job_count_with_limit + self._page_count_with_limit
        self._task_state_meta['current'] += 1
        self._task_state_meta['job_count'] = page_0.job_count
        self.update_state()
        await self.populate_details(bpage, page_0)
        if page_count > 1:
            for page_n in range(1, self._page_count_with_limit):
                page = await make_page(1, self._url, self._PageClass)
                self._task_state_meta['current'] += 1
                self.update_state()
                await self.populate_details(bpage, page)
                await asyncio.sleep(self.get_navigate_delay())
                # print(f'''{self._task_state_meta['current']}/{self._task_state_meta['total']} "current"''')
                # print("-"*10)
