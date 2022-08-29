import copy
import logging

from bs4.element import PageElement
from typing import Dict, Callable
from abc import ABC, abstractmethod


class BaseBeacon(ABC):
    company_size_map = {
        "more than 10,000": "10001>",
        "10,001+": "10001>",
        "5,001 to 10,000": "5001-10000",
        "5,001-10,000": "5001-10000",
        "1,001-5,000": "1001-5000",
        "1001 to 5,000": "1001-5000",
        "501 to 1,000": "501-1000",
        "501-1,000": "501-1000",
        "201 to 500": "201-500",
        "201-500": "201-500",
        "51 to 200": "51-200",
        "51-200": "51-200",
        "11 to 50": "11-50",
        "11-50": "11-50",
        "less than 10": "2-10",
        "2-10": "2-10",
    }

    def __init__(self, beacon: PageElement):
        self._beacon: PageElement = beacon
        self._job_post: Dict[str, str | dict] = {"company": {}}

    @property
    def dict(self):
        return self._job_post

    @abstractmethod
    def populate_from_job_card(self):
        pass

    @abstractmethod
    def populate_from_details(self, job_view_html):
        pass

    @abstractmethod
    def populate_from_company_profile(self, about_company_html, about_employees_html=None):
        """ all must be company attributes """
        pass

    def make_attribute_helper(self, dslice: dict, key: str, *commands: Callable):
        """
        Creates an optional attribute on the dslice
        and catches if the classname was not found by BeautifulSoap
        :param dslice: the dictionary to put attributes on
        :param key: attribute name
        :param commands:  functions as commands to extract attribute from a beacon:PageElement
        :return: None
        example usage: self.make_attribute('title', lambda: self._beacon.find_next('a', class_='jcs-JobTitle').text)
        """
        errors = []
        for command in commands:
            if dslice.get(key):
                break
            try:
                attribute_value = command()
                if attribute_value and attribute_value != 'None':
                    dslice[key] = str(attribute_value).strip()
            except Exception as e:
                errors.append(f' | {str(e)}')
        if not dslice.get(key):
            logging.warning(f'Error finding [{key}] for job or company {self._job_post.get("url")}'
                            f' {(e for e in errors)}')

    def make_attribute(self, name: str, *commands: Callable):
        self.make_attribute_helper(self._job_post, name, *commands)

    def make_company_attribute(self, name: str, *commands: Callable):
        self.make_attribute_helper(self._job_post['company'], name, *commands)

    def populate_company_from_bec(self, other_bec):
        self._job_post['company'] = copy.deepcopy(other_bec._job_post['company'])
