import copy
import logging

from bs4.element import PageElement
from typing import Dict, Callable
from abc import ABC, abstractmethod

from bas_app.scraper.BaseBeacon import BaseBeacon


class BaseBrowserBeacon(BaseBeacon, ABC):
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

    @abstractmethod
    def populate_from_job_card(self):
        pass

    @abstractmethod
    def populate_from_details(self, job_view_html):
        pass

    @abstractmethod
    def populate_from_company_profile(self, about_company_html, about_employees_html=None):
        """ all must be company fields """
        pass


