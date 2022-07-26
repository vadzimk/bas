from bs4.element import PageElement, ResultSet
from BaseBeacon import Beacon
from typing import List


from IndeedBeacon import IndeedBeacon
from BasePage import ThePage
from utils import make_soup, override
import re


class IndeedPage(ThePage):

    def __init__(self, page_index: int, url: str):
        super().__init__(page_index, url)
        self._job_count = self.count_total_jobs() if self._page_index == 0 else 0
        self._beacons: List[Beacon] = self.make_beacon_list()
        # self.save_beacons_csv()

    @override
    def count_total_jobs(self, ) -> int:
        count_text = self._soup.select_one('#searchCountPages').text
        m = re.search(r"of (\d+) jobs", count_text)
        return int(m.group(1))

    @override
    def make_beacon_list(self) -> List[Beacon]:
        results_list: ResultSet[PageElement] = self._soup.find_all('div', class_='job_seen_beacon')
        print(len(results_list), 'len(results_list)')
        beacons: List[Beacon] = []
        for result in results_list:
            beacons.append(IndeedBeacon(result))
            # break  # TODO remove after done testing populate_from_iframe
        return beacons
