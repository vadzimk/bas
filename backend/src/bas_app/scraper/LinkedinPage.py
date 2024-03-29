import asyncio
import logging
import math
import time

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
from bs4.element import PageElement, ResultSet
from BaseBrowserBeacon import BaseBrowserBeacon
from typing import List

from BasePage import BasePage
from LinkedinBeacon import LinkedinBeacon
from utils import SearchResultsEmpty
from utils import override, save_safe


class LinkedinPage(BasePage):
    JOBS_ON_PAGE = 25

    def __init__(self, page_index: int, url: str):
        super().__init__(page_index, url)
        self._PAGE_MULTIPLIER: int = 1
        self._url: str = f"{url}{'&start=' + str(self._PAGE_MULTIPLIER * page_index) if page_index else ''}"

    @override
    async def populate(self, bpage):

        self._soup = await self.make_beacon_soup(bpage)  # beacon soup only!!!

        logging.info(f'LinkedinPage: job count: {self._job_count}')
        self._beacons: List[BaseBrowserBeacon] = self.make_beacon_list()


    @override
    async def count_total_jobs(self, bpage) -> int:
        try:
            count_text = await bpage.locator('small.jobs-search-results-list__text').first.text_content()
            count_text = count_text.replace(' results', '').replace(' result', '').replace(',', '')
        except PlaywrightTimeoutError:  # no search results found
            logging.warning(f'Warning: no search results found in {self._url}')
            return 0
        return int(count_text)

    async def beacons_on_this_page_calc(self, bpage):
        self._job_count = await self.count_total_jobs(bpage)
        full_page_count = math.floor(self.job_count / self.JOBS_ON_PAGE)
        last_page_job_count = self.job_count - full_page_count * self.JOBS_ON_PAGE
        is_last_page = self._page_index == math.ceil(self.job_count / self.JOBS_ON_PAGE)
        return last_page_job_count if is_last_page else self.JOBS_ON_PAGE

    async def make_beacon_soup(self, bpage):
        await bpage.goto(self._url)
        try:  # make sure there are search results
            await bpage.wait_for_selector('h1:has-text("No matching jobs found.")', timeout=1000)
            raise SearchResultsEmpty(f'Search results empty on page {self._url}')
        except PlaywrightTimeoutError:
            pass  # Search results present - carry on
        """ Scrolls the left pane to load all beacons """
        beacons = bpage.locator('.jobs-search-results__list-item')
        num_beacons = await beacons.count()
        logging.info(f'{num_beacons} LinkedinPage: num_beacons on this page: {self._url}')
        num_beacons_calc = await self.beacons_on_this_page_calc(bpage)
        logging.info(f'{num_beacons_calc} LinkedinPage: num_beacons_calc on this page: {self._url}')
        try:
            for i in range(num_beacons_calc - 1):
                b = beacons.nth(i)
                await b.wait_for(state='attached', timeout=1000)  # TODO see if itmeout worked
                await b.scroll_into_view_if_needed()
            await bpage.wait_for_selector(f'.job-card-list__title >> nth={num_beacons_calc - 2}')
        except Exception as e:
            logging.error(f'LindkedinPage: Error from make_beacon_soup. While scrolling beacons. at url {self._url} {e}')
        await asyncio.sleep(1)  # wait for all cards to load

        # sometimes the classname differs
        try:
            search_results_html = await bpage.inner_html('.scaffold-layout__list', timeout=5000)
        except PlaywrightTimeoutError:
            search_results_html = await bpage.inner_html('.jobs-search__left-rail')


        logging.info(f'beacons on this page after scroll: {num_beacons}')
        # save_safe(search_results_html, str(self._page_index) + '.html')
        return BeautifulSoup(search_results_html, 'html.parser')

    @override
    def make_beacon_list(self) -> List[BaseBrowserBeacon]:
        results_list: ResultSet[PageElement] = self._soup.find_all('li', class_='jobs-search-results__list-item')
        logging.info(f'{len(results_list)} len(results_list)')
        beacons: List[BaseBrowserBeacon] = []
        for result in results_list:
            if 'Promoted' not in result.text:  # Filter out Promoted listings TODO do I need a frontend flag for it?
                beacons.append(LinkedinBeacon(result))
        return beacons
