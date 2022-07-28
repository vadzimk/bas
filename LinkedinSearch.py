import math
import time
import urllib
from enum import Enum
from pprint import pprint
from typing import List

from bs4 import BeautifulSoup

from LinkedinPage import LinkedinPage
from utils import override

from BaseSearch import BaseSearch
from playwright.sync_api import sync_playwright
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

    def __init__(self,
                 what,
                 where,
                 age: Filters.Age = Filters.Age.ALL,
                 radius: Filters.Radius = Filters.Radius.ALL,
                 experience: List[Filters.Experience] = [Filters.Experience.ALL]):
        super().__init__(what, where, age, radius, experience)
        self._url = f"""https://www.linkedin.com"""
        self._pages = self.flip_pages()
        self.populate_details()

    def populate_details(self):
        """ Populate details form 'iframe' """
        with sync_playwright() as pwt:
            bpage = self.create_session(pwt)
            for page_index, p in enumerate(self._pages):
                if page_index == 1: break  # TODO remove it, this is for testiong only
                for b in p.beacons:
                    try:
                        job_url = b.dict['url']
                        bpage.goto(job_url)
                        bpage.locator('span.artdeco-button__text:has-text("See more")').click()
                        job_view = bpage.locator('.job-view-layout')
                        job_view_html = job_view.inner_html()
                        b.populate_from_details(job_view_html)
                    except Exception as e:
                        print(f'Error going to {job_url}', e)
                    time.sleep(3)
                    try:
                        company_url = b.dict['company_profile_url']
                        # replaced by going directly to the about
                        # bpage.locator('footer.artdeco-card__actions >> span:has-text("See all details")').click()
                        bpage.goto(f'{company_url}about/')
                        about_company = bpage.locator('div.org-grid__content-height-enforcer')
                        about_company_html = about_company.inner_html()

                        # replaced by going directly to the people
                        # bpage.locator('li.org-page-navigation__item > a:has-text("People")').click()
                        bpage.goto(f'{company_url}people/')
                        bpage.wait_for_selector('div.insight-container')
                        about_employees = bpage.locator('div.org-grid__content-height-enforcer')
                        about_employees_html = about_employees.inner_html()

                        b.populate_from_company_profile(about_company_html, about_employees_html)
                    except Exception as e:
                        print(f'Error going to {company_url}', e)
                    print('job post:')
                    pprint(b.dict)
                    time.sleep(3)

    # @override
    # def old_flip_pages(self):
    #     pages: List[IndeedPage] = []
    #     page0 = LinkedinPage(0, self._url)
    #     pages.append(page0)
    #     # page_count = math.ceil(page0.job_count / self.JOBS_ON_PAGE)
    #     # print(page_count)
    #     # if page_count > 1:
    #     #     for page_n in range(1, page_count + 1):
    #     #         page = IndeedPage(page_n, self._url)
    #     #         pages.append(page)
    #     return pages

    def create_session(self, pwt):
        browser = pwt.chromium.launch(args=[''],
                                      headless=True,
                                      # slow_mo=50
                                      )
        load_dotenv()
        email = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        bpage = browser.new_page(no_viewport=True)
        bpage.goto(self._url)
        bpage.fill('input#session_key', email)
        bpage.fill('input#session_password', password)
        bpage.click('button[type=submit]')
        return bpage

    @override
    def flip_pages(self):
        pages: List[LinkedinPage] = []
        with sync_playwright() as p:
            bpage = self.create_session(p)
            url = f"""{self._url}/jobs/search/?{self._radius}{self.attributes()}{self._age}&keywords={urllib.parse.quote(self._query)}&location={urllib.parse.quote(self._location)}"""
            page0 = LinkedinPage(0, url, bpage)
            pages.append(page0)
            page_count = math.ceil(page0.job_count / page0.JOBS_ON_PAGE)
            print(page_count)
            if page_count > 1:
                for page_n in range(1, page_count + 1):
                    print('page_n', page_n)
                    page = LinkedinPage(page_n, url, bpage)
                    pages.append(page)
                    print('-' * 10)
                    time.sleep(3)
                    if page_n == 1:
                        break  # TODO remove this line, it is to limit pages for test
            return pages

    def attributes(self) -> str:
        """
        combines education and experience to pass in the query string
        :return: string of the form '&sc=0kf%3Aattr(EXSNN%7CFCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)explvl(SENIOR_LEVEL)%3B' or empty string
        """
        attributes = ",".join(self._experience)
        return f'{"&f_E=" if attributes else ""}{urllib.parse.quote(attributes)}'
