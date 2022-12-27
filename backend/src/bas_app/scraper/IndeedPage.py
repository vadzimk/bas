import asyncio
import logging
import traceback

import requests
from bs4 import BeautifulSoup
from bs4.element import PageElement, ResultSet
from BaseBrowserBeacon import BaseBrowserBeacon
from typing import List

from IndeedBeacon import IndeedBeacon
from BasePage import BasePage
from utils import override, save_safe, make_soup, SearchResultsEmpty
import re
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


class IndeedPage(BasePage):
    JOBS_ON_PAGE = 15

    def __init__(self, page_index: int, url: str):
        super().__init__(page_index, url)
        self._PAGE_MULTIPLIER: int = 10
        self._url: str = f"{url}{'&start=' + str(self._PAGE_MULTIPLIER * page_index) if page_index else ''}"
        logging.info(f"IndeedPage:  going to url: {self._url}")

    @override
    async def populate(self, bpage):
        # self._soup = make_soup(self._url, f'response{self._page_index}.html')
        try:
            await bpage.locator('button.popover-x-button-close').click(timeout=5000)
            logging.info("Popup on indeed page")
        except PlaywrightTimeoutError as e:
            pass  # No popup on current page
        self._soup = await self.make_beacon_soup(bpage)
        if self._soup.find('.jobsearch-NoResult-messageContainer'):
            raise SearchResultsEmpty("Search results empty")
        self._job_count = self.count_total_jobs() if self._page_index == 0 else 0
        print('job_count', self._job_count)
        self._beacons: List[BaseBrowserBeacon] = self.make_beacon_list()
        # self.save_beacons_csv()

    @override
    def count_total_jobs(self, ) -> int:
        count_text = (self._soup.select_one('#searchCountPages')
                      or
                      self._soup.select_one('.jobsearch-JobCountAndSortPane-jobCount')).text

        # m = re.search(r"of (\d+) jobs", count_text)
        m = re.search(r"(\d+) jobs", count_text)
        return int(m.group(1))

    async def make_beacon_soup(self, bpage):
        await bpage.goto(self._url)
        await asyncio.sleep(1)  # wait for page to load data
        text = await bpage.inner_html('html')
        return BeautifulSoup(text, 'html.parser')

    @override
    def make_beacon_list(self) -> List[BaseBrowserBeacon]:
        results_list: ResultSet[PageElement] = self._soup.find_all('div', class_='job_seen_beacon')
        logging.info(f'len(results_list): {len(results_list)}')
        beacons: List[BaseBrowserBeacon] = []
        for result in results_list:
            beacons.append(IndeedBeacon(result))
        return beacons
