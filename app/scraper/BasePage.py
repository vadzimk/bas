from bs4 import BeautifulSoup

from BaseBeacon import BaseBeacon
from typing import List, Optional
from pandas import pandas as pd
from pandas import DataFrame
from app import db
from app.models import Job, Company

from abc import ABC, abstractmethod


class BasePage(ABC):
    JOBS_ON_PAGE = None

    def __init__(self, page_index: int, url: str):
        self._page_index = page_index
        self._soup: Optional[BeautifulSoup] = None
        self._job_count: Optional[int] = None
        self._beacons: Optional[List[BaseBeacon]] = None

    @property
    def job_count(self) -> int:
        return self._job_count

    @property
    def beacons(self) -> List[BaseBeacon]:
        return self._beacons

    @abstractmethod
    def count_total_jobs(self, ) -> int:
        """
        :return: number of jobs that the Indeed query returns
        """
        pass

    @abstractmethod
    def make_beacon_list(self) -> List[BaseBeacon]:
        pass

    def save_beacons_csv(self):
        df: DataFrame = pd.DataFrame(beacon.dict for beacon in self._beacons)
        df.to_csv(f'out/page{self._page_index}.csv')

    @abstractmethod
    async def populate(self, bpage):
        """ makes beacon list and saves to self._beacons """
        pass

    def save_beacons_db(self):
        """ saves self._beacons to db"""
        for b in self._beacons:
            job = Job.query.filter_by(url=b.dict.get('url')).first()
            if not job:
                job_attributes = {k: v for k, v in b.dict.items() if k != 'company'}  # copy only job attributes
                job = Job(**job_attributes)
                db.session.add(job)
        db.session.commit()
