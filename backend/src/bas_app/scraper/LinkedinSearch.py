import asyncio
import logging
import sys
import urllib
from enum import Enum

from typing import List, Awaitable, Callable
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from LinkedinPage import LinkedinPage
from bas_app.models import Task
from utils import AccountBlocked, AccountNotFound, PageCrashed
from utils import override

from BaseBrowserSearch import BaseBrowserSearch

import os
from dotenv import load_dotenv


class LinkedinSearch(BaseBrowserSearch):
    NAVIGATE_DELAY = 30

    class Filters:
        class Radius(str, Enum):
            EXACT = 'distance=0'
            FIVE = 'distance=5'
            TEN = 'distance=10'
            TWENTY_FIVE = 'distance=25'
            FIFTY = 'distance=50'
            HUNDRED = 'distance=100'
            ALL = ''

        class Experience(str, Enum):
            INTERNSHIP = '1'
            ENTRY_LEVEL = '2'
            ASSOCIATE = '3'
            MID_SENIOR = '4'
            DIRECTOR = '5'
            EXECUTIVE = '6'
            ALL = ''

        class Age(str, Enum):
            PAST_MONTH = '&f_TPR=r2592000'
            PAST_WEEK = '&f_TPR=r604800'
            PAST_24H = '&f_TPR=r86400'
            ALL = ''

    def __init__(self, *,
                 what,
                 where,
                 age: Filters.Age = Filters.Age.ALL,
                 radius: Filters.Radius = Filters.Radius.ALL,
                 experience: List[Filters.Experience] = [Filters.Experience.ALL],
                 limit: int = sys.maxsize,
                 linkedin_credentials: dict,
                 user_id: int = None,
                 search_model_id: int = None,
                 task_id: str = None,
                 ):
        super().__init__(what=what, where=where, age=age, radius=radius, experience=experience, limit=limit, user_id=user_id, search_model_id=search_model_id, task_id=task_id)

        self._base_url = f"""https://www.linkedin.com"""
        self._url = f"""{self._base_url}/jobs/search/?{self._radius}{self.attributes()}{self._age}&keywords={urllib.parse.quote(self._query)}&location={urllib.parse.quote(self._location)}"""
        self._PageClass = LinkedinPage
        self._linkedin_credentials = linkedin_credentials

    @override
    @staticmethod
    async def populate_job_post_details(beacon, job_url, bpage):
        try:
            await bpage.goto(job_url)
            try:
                job_page_not_found = bpage.locator(
                    'div:has-text("The job you were looking for was not found. Redirecting you to the home page")')
                if job_page_not_found:
                    logging.error(job_page_not_found)
                await bpage.locator('span.artdeco-button__text:has-text("See more")').click(timeout=2000)
            except PlaywrightTimeoutError as e:
                logging.warning(e)
            job_view = bpage.locator('.job-view-layout')
            job_view_html = await job_view.inner_html()
            beacon.populate_from_details(job_view_html)
        except Exception as e:
            logging.error(f'Error going to job_url {job_url} {e}')
            if "Navigation failed because page crashed!" in str(e):
                raise PageCrashed(str(e))

    @override
    @staticmethod
    async def populate_company_details(beacon, company_profile_url, bpage):
        try:
            await bpage.goto(f'{company_profile_url}about/')
            about_company = bpage.locator('div.org-grid__content-height-enforcer')
            about_company_html = await about_company.inner_html()
            await bpage.goto(f'{company_profile_url}people/')
            await bpage.wait_for_selector('div.insight-container')
            about_employees = bpage.locator('div.org-grid__content-height-enforcer')
            about_employees_html = await about_employees.inner_html()

            beacon.populate_from_company_profile(about_company_html, about_employees_html)
        except Exception as e:
            logging.error(f'Error going to company_url {company_profile_url} {e}')
            if "Navigation failed because page crashed!" in str(e):
                raise PageCrashed(str(e))

    async def get_verification_code(self):
        """ queries table Task every 2s until verification_code exists"""
        verification_code = Task.query.get(self._task_id).verification_code
        while not verification_code:
            await asyncio.sleep(2)
            verification_code = Task.query.get(self._task_id).verification_code
        return verification_code

    @override
    async def create_session(self,
                             bpage,
                             task_update_state):
        """
        logs into the website and returns the playwright_page
        :raises AccountBlocked, AccountNotFound
        """
        load_dotenv()
        self._task_update_state = task_update_state
        email = self._linkedin_credentials.get('email')
        password = self._linkedin_credentials.get('password')
        await bpage.goto(self._base_url)
        print(email, password)
        await bpage.fill('input#session_key', email)
        await asyncio.sleep(1)
        await bpage.fill('input#session_password', password)
        await asyncio.sleep(1)
        await bpage.click('button[type=submit]')

        try:
            await bpage.wait_for_selector('text=The login attempt seems suspicious. To finish signing in please enter the verification code we sent to your email address.', timeout=2000)
            self._task_state_meta["task_id"] = self._task_id
            self._task_state_meta["email"] = email
            self._task_update_state(state='VERIFICATION', meta=self._task_state_meta)
            print("waiting for code")
            verification_code = await self.get_verification_code()
            print("verification_code from db", verification_code)
            await bpage.fill('input[name=pin]', verification_code)
            await bpage.click('button[type=submit]')
            self._task_update_state(state='VERIFYING', meta=self._task_state_meta)
        except PlaywrightTimeoutError:
            pass  # security passed

        try:
            await bpage.wait_for_selector('text=Access to your account has been temporarily restricted', timeout=2000)
            raise AccountBlocked(f"Linkedin account blocked: {email}")
        except PlaywrightTimeoutError:
            pass  # account not blocked

        try:
            await bpage.wait_for_selector('text=Couldn’t find a LinkedIn account associated with this email',
                                          timeout=2000)
            raise AccountNotFound(f"Linkedin account not found: {email}")
        except PlaywrightTimeoutError:
            pass  # account exists

        return bpage


    def attributes(self) -> str:
        """
        combines education and experience to pass in the query string
        :return: string of the form '&sc=0kf%3Aattr(EXSNN%7CFCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)explvl(SENIOR_LEVEL)%3B' or empty string
        """
        attributes = ",".join(self._experience)
        return f'{"&f_E=" if attributes else ""}{urllib.parse.quote(attributes)}'

    @override
    def run_api(self, task_update_state):
        # not applicable
        raise NotImplementedError
