from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

query = """react AND (python OR node) AND NOT (ruby OR ".NET") developer AND NOT (citizen OR Citizen OR "green card" OR "Green Card") and NOT (senior OR Senior OR lead OR Lead) AND NOT ("CyberCoders" OR "Jobot")"""

location = """Los Angeles, California, United States"""


def crawl():
    global query, location
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        email = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        page = browser.new_page()
        page.goto('https://www.linkedin.com')
        page.fill('input#session_key', email)
        page.fill('input#session_password', password)
        page.click('button[type=submit]')
        page.goto('https://www.linkedin.com/jobs/')
        page.locator(
            'input.jobs-search-box__text-input.jobs-search-box__keyboard-text-input[aria-label="Search by title, skill, or company"]').first.fill(
            query)
        page.locator(
            'input.jobs-search-box__text-input[aria-label="City, state, or zip code"]').first.fill(
            location)
        page.locator('.basic-typeahead__triggered-content[role="listbox"]').locator(f'text={location}').first.click()
        # page.locator('button.jobs-search-box__submit-button').click()

        search_results_html = page.inner_html('.jobs-search-results')
        # print(search_results_html)
        soup = BeautifulSoup(search_results_html, 'html.parser')
        titles = soup.find_all('a', class_='job-card-list__title')
        print(titles)


if __name__ == '__main__':
    crawl()
