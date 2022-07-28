from bs4 import BeautifulSoup

from BaseBeacon import BaseBeacon
from typing import List, Optional
from pandas import pandas as pd
from pandas import DataFrame


from abc import ABC, abstractmethod

class BasePage(ABC):

    def __init__(self, page_index: int, url: str):
        self._page_index = page_index


        self._soup: Optional[BeautifulSoup] = None
        self._job_count: Optional[int] = None
        self._beacons: Optional[List[BaseBeacon]] = None

    @property
    def job_count(self):
        return self._job_count

    @property
    def beacons(self):
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

