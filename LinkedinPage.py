import math
import time

from bs4 import BeautifulSoup
from bs4.element import PageElement, ResultSet
from BaseBeacon import BaseBeacon
from typing import List

from BasePage import BasePage
from LinkedinBeacon import LinkedinBeacon
from utils import make_soup, override, save_safe
import re


class LinkedinPage(BasePage):
    JOBS_ON_PAGE = 25

    def __init__(self, page_index: int, url: str):
        super().__init__(page_index, url)
        self._PAGE_MULTIPLIER: int = 1
        self._url: str = f"{url}{'&start=' + str(self._PAGE_MULTIPLIER * page_index) if page_index else ''}"

    @override
    async def populate(self, bpage):
        self._soup = await self.make_beacon_soup(bpage)  # beacon soup only!!!
        self._job_count = self.count_total_jobs() if self._page_index == 0 else 0
        print('LinkedinPage: job count: ', self._job_count)
        self._beacons: List[BaseBeacon] = self.make_beacon_list()
        # self.save_beacons_csv()

    @override
    def count_total_jobs(self, ) -> int:
        count_text = self._soup.find('small', class_='jobs-search-results-list__text').text
        count_text = count_text.replace(' results', '').replace(' result', '').replace(',', '')
        return int(count_text)

    async def make_beacon_soup(self, bpage):
        await bpage.goto(self._url)
        # Search input replaced by url
        # self._browser_page.locator(
        #     'input.jobs-search-box__text-input.jobs-search-box__keyboard-text-input[aria-label="Search by title, skill, or company"]').first.fill(
        #     self._query)
        # self._browser_page.locator(
        #     'input.jobs-search-box__text-input[aria-label="City, state, or zip code"]').first.fill(
        #     self._location)
        # self._browser_page.locator('.basic-typeahead__triggered-content[role="listbox"]').locator(
        #     f'text={self._location}').first.click()

        # scrollable = self._browser_page.locator('.jobs-search-results')
        # scrollable.evaluate('(e) => e.scrollTop = e.scrollHeight')

        """ Scrolls the left pane to load all beacons """
        beacons = bpage.locator('.jobs-search-results__list-item')
        num_beacons = await beacons.count()
        print(num_beacons, 'LinkedinPage: num_beacons on this page: ', self._url)
        for i in range(num_beacons):
            try:
                b = beacons.nth(i)
                await b.wait_for(state='attached')
                await b.scroll_into_view_if_needed()
            except Exception as e:
                print('LindkedinPage: Error from make_beacon_soup: ', e)
        time.sleep(3) # wait for all cards to load

        search_results_html = await bpage.inner_html('.jobs-search__left-rail')
        print('beacons on this page after scroll: ', num_beacons)
        # self._browser_page.wait_for_selector(f'.job-card-list__title >> nth={num_beacons-1}')
        save_safe(search_results_html, str(self._page_index) + '.html')
        return BeautifulSoup(search_results_html, 'html.parser')

    @override
    def make_beacon_list(self) -> List[BaseBeacon]:
        results_list: ResultSet[PageElement] = self._soup.find_all('li', class_='jobs-search-results__list-item')
        print(len(results_list), 'len(results_list)')
        beacons: List[BaseBeacon] = []
        for result in results_list:
            beacons.append(LinkedinBeacon(result))
            # break  # TODO remove after done testing populate_from_iframe
        return beacons
