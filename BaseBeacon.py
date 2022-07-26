from bs4.element import PageElement
from typing import Dict, Callable
from abc import ABC, abstractmethod


class Beacon(ABC):
    def __init__(self, beacon: PageElement):
        self._beacon: PageElement = beacon
        self._job_post: Dict[str, str] = {}

    @property
    def dict(self):
        return self._job_post

    @abstractmethod
    def populate_from_job_card(self):
        pass

    def make_attribute(self, name: str, command: Callable):
        """
        Creates an optional attribute on the self._job_post dict
        and catches if the classname was not found by BeautifulSoap
        :param name: attribute name
        :param command: lambda function as a command to extract attribute from a beacon:PageElement
        :return: None
        example usage: self.make_attribute('title', lambda: self._beacon.find_next('a', class_='jcs-JobTitle').text)
        """
        attribute_value = None
        try:
            attribute_value = command()
        except Exception as e:
            print(f'Error finding {name} for job {self._job_post["title"]}', e)
        self._job_post[name] = attribute_value

    @abstractmethod
    def populate_from_iframe(self):
        pass
