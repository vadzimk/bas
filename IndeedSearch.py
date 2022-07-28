import math
import urllib
from enum import Enum
from typing import List
from utils import override
from IndeedPage import IndeedPage
from BaseSearch import BaseSearch


class IndeedSearch(BaseSearch):
    class Filters:
        class Radius(str, Enum):
            EXACT = '&radius=0'
            FIVE = '&radius=5'
            TEN = '&radius=10'
            FIFTEEN = '&radius=15'
            TWENTY_FIVE = '&radius=25'
            HUNDRED = '&radius=100'
            ALL = ''

        class Experience(str, Enum):
            ENTRY = 'explvl(ENTRY_LEVEL)'
            MID = 'explvl(MID_LEVEL)'
            SENIOR = 'explvl(SENIOR_LEVEL)'
            ALL = ''

        class Education(str, Enum):
            SCHOOL = 'attr(FCGTU%7CQJZM9%252COR)',
            ASSOCIATES = 'attr(FCGTU%7CQJZM9%7CUTPWG%252COR)',
            BACHELORS = 'attr(FCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)',
            MASTERS = 'attr(EXSNN%7CFCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)',
            ALL = ''

        class Age(str, Enum):
            LAST = 'last'
            ONE = '1'
            TREE = '3'
            SEVEN = '7'
            FOURTEEN = '14'
            ALL = ''



    def __init__(self,
                 what,
                 where,
                 age=Filters.Age.ALL,
                 radius=Filters.Radius.ALL,
                 experience=Filters.Experience.ALL,
                 education=Filters.Education.ALL):
        super().__init__(what, where, age, radius, experience, education)
        self._url = f"""https://www.indeed.com/jobs?q={urllib.parse.quote(self._query)}&l={urllib.parse.quote(self._location)}{self.attributes()}{self._radius}&fromage={self._age}"""
        self._pages = self.flip_pages()

    @override
    def flip_pages(self):
        pages: List[IndeedPage] = []
        page0 = IndeedPage(0, self._url)
        pages.append(page0)
        page_count = math.ceil(page0.job_count / page0.JOBS_ON_PAGE)
        print('page_count', page_count)
        if page_count > 1:
            for page_n in range(1, page_count + 1):
                page = IndeedPage(page_n, self._url)
                pages.append(page)
        return pages

    def attributes(self) -> str:
        """
        combines education and experience to pass in the query string
        :return: string of the form '&sc=0kf%3Aattr(EXSNN%7CFCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)explvl(SENIOR_LEVEL)%3B' or empty string
        """
        attributes = f'{self._education}{self._experience}'
        return f'{"&sc=0kf%3A" if attributes else ""}{attributes}{"%3B" if attributes else ""}'
