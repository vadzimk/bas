import copy
import logging

from typing import Dict, Callable
from abc import ABC


class BaseBeacon(ABC):
    def __init__(self):
        self._job_post: Dict[str, str | dict] = {"company": {}}

    @property
    def dict(self):
        return self._job_post

    @property
    def job_attributes_only(self) -> dict:
        """
        :return dict containing fields of job and not company """
        job_attributes = {k: v for k, v in self.dict.items() if k != 'company'}  # copy only job fields
        return job_attributes

    def make_attribute_helper(self, dslice: dict, key: str, *commands: Callable):
        """
        Creates an optional attribute on the dslice
        and catches if the classname was not found by BeautifulSoap
        :param dslice: the dictionary to put fields on
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


