from abc import ABC, abstractmethod
from typing import List, Optional

from BasePage import BasePage


class BaseSearch(ABC):
    def __init__(self, what, where, age, radius, experience, education=''):
        self._query = what
        self._location = where
        self._age = age
        self._radius = radius
        self._experience = experience
        self._education = education
        self._pages: Optional[List[BasePage]] = None

    @property
    def pages(self):
        return self._pages

    @abstractmethod
    def flip_pages(self):
        pass

    @abstractmethod
    async def populate(self, bpage):
        pass