from bs4.element import PageElement, ResultSet
from Beacon import Beacon
from typing import List
from pandas import pandas as pd
from pandas import DataFrame
from utils import make_soup
import re


class IndeedPage:

    def __init__(self, page_index: int, url: str):
        self._page_index = page_index
        self._PAGE_MULTIPLIER: int = 10
        self._url: str = f"{url}{'&start=' + str(self._PAGE_MULTIPLIER * page_index) if page_index else ''}"
        self._soup = make_soup(self._url, f'response{self._page_index}.html')
        self._job_count = self.count_total_jobs() if self._page_index == 0 else 0
        self._beacons: List[Beacon] = self.make_beacon_list()
        # self.save_beacons_csv()

    @property
    def job_count(self):
        return self._job_count

    @property
    def beacons(self):
        return self._beacons

    def count_total_jobs(self, ) -> int:
        """
        :return: number of jobs that the Indeed query returns
        """
        count_text = self._soup.select_one('#searchCountPages').text
        m = re.search(r"of (\d+) jobs", count_text)
        return int(m.group(1))

    def make_beacon_list(self) -> List[Beacon]:
        results_list: ResultSet[PageElement] = self._soup.find_all('div', class_='job_seen_beacon')
        print(len(results_list), 'len(results_list)')
        beacons: List[Beacon] = []
        for result in results_list:
            beacons.append(Beacon(result))
            # break  # TODO remove after done testing populate_from_iframe
        return beacons

    def save_beacons_csv(self):
        df: DataFrame = pd.DataFrame(beacon.dict for beacon in self._beacons)
        df.to_csv(f'out/page{self._page_index}.csv')
