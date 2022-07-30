import os
import re
import shutil
from pathlib import Path

import cfscrape
import cloudscraper
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def use_cloudscraper(url):
    scraper = cloudscraper.create_scraper()
    text = scraper.get(url).text
    print('content', text)
    return text


def use_cfscrape(url):
    scraper = cfscrape.create_scraper(delay=10)
    text = scraper.get(url).text
    print('content', text)
    return text


def use_requests(url):
    user_agent1 = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0'  # https://webbrowsertools.com/useragent/
    user_agent2 = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    headers = {'User-Agent': user_agent2}
    res = requests.get(url, headers)
    print('status code', res.status_code, url)
    return res.text


def use_playwright(url):
    with sync_playwright() as pwt:
        browser = pwt.chromium.launch(headless=False)
        bpage = browser.new_page()
        bpage.goto(url)
        text = bpage.inner_html('html')
        return text


def make_soup(url, export_filename):
    html = use_playwright(url)
    save_safe(html, export_filename)
    return BeautifulSoup(html, 'html.parser')


def save_safe(text, filename):
    """
    saves text to the specified file in the out folder while replacing bad path characters in the filename
    :param text: text to save
    :param filename:
    """
    filename = re.sub(r'[^\w\-_\. ]', '_', filename)
    with open(f'out/{filename}', 'w') as file:
        file.write(text)


def cleanup(out_dir='out'):
    if os.path.exists(out_dir) and os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
        print("Old project flies deleted.")


def create_project(out_dir='out'):
    # create directory for the project
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    # Path(PR.DIR_TABULATED_CSV).mkdir(parents=True, exist_ok=True)
    # Path(PR.DIR_PRODUCT_TABLES).mkdir(parents=True, exist_ok=True)
    # Path(PR.DIR_TREATED_ROWS).mkdir(parents=True, exist_ok=True)

    if os.path.exists(out_dir) and os.path.isdir(out_dir):
        print(f"New project directory {out_dir} created")
    else:
        print(f"New project directory {out_dir} creation FAILED")


def override(f):
    return f


# ----------- Task Runtime Errors -------------
class TaskError():
    pass


class SearchResultsEmpty(RuntimeError, TaskError):
    pass


class AccountBlocked(RuntimeError, TaskError):
    pass


# ---------------------------------------------
