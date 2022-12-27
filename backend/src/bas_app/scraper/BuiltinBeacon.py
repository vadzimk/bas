import asyncio
import copy
import logging
import re
import time

from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag

from BaseBeacon import BaseBeacon
from utils import make_soup, override, save_safe, replace_p_br_p, age_to_date
from markdownify import markdownify, MarkdownConverter


# Create shorthand method for conversion
def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


class BuiltinBeacon(BaseBeacon):
    def __init__(self):
        super().__init__()

    def parse_job(self, job: dict):
        self.make_attribute('title', lambda: job.get("title"))
        self.make_attribute('url', lambda: f'https://builtin{"la"}.com{job.get("alias")}') # TODO for other locations replace the suffix la
        self.make_attribute('description_markdown', lambda: markdownify(job.get("body")))
        self.make_attribute('description_html', lambda: job.get("body"))
        self.make_attribute('description_text', lambda: BeautifulSoup(job.get("body")).text)
        self.make_attribute('created_str', lambda: job.get("recency_count"))
        self.make_attribute('job_type', lambda: str(job.get("working_option")))

    def parse_company(self, company:dict):
        self.make_company_attribute('name', lambda: company.get("title"))
        self.make_company_attribute('industry', lambda: ", ".join([i.get("name") for i in company.get("industries")]))
        self.make_company_attribute('size', lambda: company.get("total_employees"))
        self.make_company_attribute('overview', lambda: company.get("mini_description"))
        self.make_company_attribute('number_employees', lambda: company.get("total_employees"))
        self.make_company_attribute('location', lambda: f'{company.get("state")}, {company.get("city")}, {company.get("street_address_1")}')
        self.make_company_attribute('main_country_number_employees', lambda: company.get("local_employees"))
        self.make_company_attribute('profile_url', lambda: f'https://builtin.com{company.get("alias")}')
        self.make_company_attribute('homepage_url', lambda: company.get("url"))



