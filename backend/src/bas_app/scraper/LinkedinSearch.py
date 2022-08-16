import logging
import urllib
from enum import Enum

from typing import List
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

from LinkedinPage import LinkedinPage
from utils import AccountBlocked
from utils import override

from BaseSearch import BaseSearch

import os
from dotenv import load_dotenv




class LinkedinSearch(BaseSearch):
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
                 experience: List[Filters.Experience] = [Filters.Experience.ALL]):
        super().__init__(what, where, age, radius, experience)
        self._base_url = f"""https://www.linkedin.com"""
        self._url = f"""{self._base_url}/jobs/search/?{self._radius}{self.attributes()}{self._age}&keywords={urllib.parse.quote(self._query)}&location={urllib.parse.quote(self._location)}"""
        self._PageClass = LinkedinPage

    @override
    @staticmethod
    async def populate_job_post_details(beacon, job_url, bpage):
        try:
            await bpage.goto(job_url)
            await bpage.locator('span.artdeco-button__text:has-text("See more")').click()
            job_view = bpage.locator('.job-view-layout')
            job_view_html = await job_view.inner_html()
            beacon.populate_from_details(job_view_html)
        except Exception as e:
            logging.error(f'Error going to {job_url} {e}')

    @override
    @staticmethod
    async def populate_company_details(beacon, company_url, bpage):
        try:
            await bpage.goto(f'{company_url}about/')
            about_company = bpage.locator('div.org-grid__content-height-enforcer')
            about_company_html = await about_company.inner_html()
            await bpage.goto(f'{company_url}people/')
            await bpage.wait_for_selector('div.insight-container')
            about_employees = bpage.locator('div.org-grid__content-height-enforcer')
            about_employees_html = await about_employees.inner_html()

            beacon.populate_from_company_profile(about_company_html, about_employees_html)
        except Exception as e:
            logging.error(f'Error going to {company_url} {e}')

    @override
    async def create_session(self, bpage):
        """ logs into the website and returns the bpage"""
        load_dotenv()
        email = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        await bpage.goto(self._base_url)
        await bpage.fill('input#session_key', email)
        await bpage.fill('input#session_password', password)
        await bpage.click('button[type=submit]')
        try:
            await bpage.wait_for_selector('text=Access to your account has been temporarily restricted', timeout=10000)
            raise AccountBlocked("Linkedin account blocked need to recreate")
        except PlaywrightTimeoutError:
            pass  # account not blocked
        return bpage

    def attributes(self) -> str:
        """
        combines education and experience to pass in the query string
        :return: string of the form '&sc=0kf%3Aattr(EXSNN%7CFCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)explvl(SENIOR_LEVEL)%3B' or empty string
        """
        attributes = ",".join(self._experience)
        return f'{"&f_E=" if attributes else ""}{urllib.parse.quote(attributes)}'
