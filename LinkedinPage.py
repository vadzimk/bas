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

    def __init__(self, page_index: int, url: str, browser_page):
        super().__init__(page_index, url)
        self._browser_page = browser_page
        # self._query = query
        # self._location = location
        self._PAGE_MULTIPLIER: int = 1
        self._url: str = f"{url}{'&start=' + str(self._PAGE_MULTIPLIER * page_index) if page_index else ''}"
        self._soup = self.make_beacon_soup()  # beacon soup only!!!
        self._job_count = self.count_total_jobs() if self._page_index == 0 else 0
        print('job count', self._job_count)
        self._beacons: List[BaseBeacon] = self.make_beacon_list()
        # self.save_beacons_csv()

    @override
    def count_total_jobs(self, ) -> int:
        count_text = self._soup.find('small', class_='jobs-search-results-list__text').text
        count_text = count_text.replace(' results', '').replace(' result', '').replace(',', '')
        return int(count_text)

    def make_beacon_soup(self):
        self._browser_page.goto(self._url)
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
        beacons = self._browser_page.locator('.jobs-search-results__list-item')
        num_beacons = beacons.count()
        print('num_beacons on this page: ', num_beacons)
        for i in range(num_beacons):  # TODO this will fail on the last page
            try:
                b = beacons.nth(i)
                b.wait_for(state='attached')
                b.scroll_into_view_if_needed()
                content = b.locator('.artdeco-entity-lockup__content').wait_for(state='attached')
            except Exception as e:
                print('Error', e)
        time.sleep(3) # wait for all cards to load

        search_results_html = self._browser_page.inner_html('.jobs-search__left-rail')
        print('beacons on this page: ', num_beacons)
        # self._browser_page.wait_for_selector(f'.job-card-list__title >> nth={num_beacons-1}')
        save_safe(search_results_html, str(self._page_index) + '.html')
        return BeautifulSoup(search_results_html, 'html.parser')

    @override
    def make_beacon_list(self) -> List[BaseBeacon]:
        results_list: ResultSet[PageElement] = self._soup.find_all('li', class_='jobs-search-results__list-item')
        print(len(results_list), 'len(results_list)')
        beacons: List[BaseBeacon] = []
        for result in results_list:
            beacons.append(LinkedinBeacon(result, self._browser_page))
            # break  # TODO remove after done testing populate_from_iframe
        return beacons
