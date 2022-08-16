import logging
import os
import re
import shutil
from pathlib import Path

import cfscrape
import cloudscraper
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from datetime import date, timedelta

from BaseBeacon import BaseBeacon


def use_cloudscraper(url):
    scraper = cloudscraper.create_scraper()
    text = scraper.get(url).text
    logging.debug(f'content {text}')
    return text


def use_cfscrape(url):
    scraper = cfscrape.create_scraper(delay=10)
    text = scraper.get(url).text
    logging.debug(f'content {text}')
    return text


def use_requests(url):
    user_agent1 = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0'  # https://webbrowsertools.com/useragent/
    user_agent2 = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    headers = {'User-Agent': user_agent2}
    res = requests.get(url, headers)
    logging.debug(f'status code {res.status_code} {url}')
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
        logging.info("Old project flies deleted.")


def create_project(out_dir='out'):
    # create directory for the project
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    # Path(PR.DIR_TABULATED_CSV).mkdir(parents=True, exist_ok=True)
    # Path(PR.DIR_PRODUCT_TABLES).mkdir(parents=True, exist_ok=True)
    # Path(PR.DIR_TREATED_ROWS).mkdir(parents=True, exist_ok=True)

    if os.path.exists(out_dir) and os.path.isdir(out_dir):
        logging.info(f"New project directory {out_dir} created")
    else:
        logging.critical(f"New project directory {out_dir} creation FAILED")


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

def replace_p_br_p(html_repr):
    """ replaces <p><br>\n</p>  to <br></br>"""
    dsoup = BeautifulSoup(html_repr, 'html.parser')
    ps = dsoup.find_all('p')
    for i, p in enumerate(ps):
        if p.string is None and p.find('br') is not None:
            br_tag = dsoup.new_tag("br")
            p.replaceWith(br_tag)
            br_tag.insert_after(dsoup.new_tag("br"))
    return dsoup


def filter_attributes_job(b: BaseBeacon) -> dict:
    """
    :argument b beacon obj
    :return dict containing attributes of job and not company """
    job_attributes = {k: v for k, v in b.dict.items() if k != 'company'}  # copy only job attributes
    return job_attributes


def age_to_date(age):
    if age == 'Today' \
            or age =='Just posted' \
            or 'hours ago' in age:
        date_value = str(date.today())
    elif '+ days ago' in age:
        n_days_ago = int(age.replace('+ days ago', '').strip()) + 14
        date_value = date.today() - timedelta(n_days_ago)
    elif 'day ago' in age \
            or 'days ago' in age:
        n_days_ago = int(age.replace('days ago', '').replace('day ago', '').strip())
        date_value = date.today() - timedelta(n_days_ago)
    elif 'weeks ago' in age or 'week ago' in age:
        n_days_ago = int(age.replace('weeks ago', '').replace('week ago', '').strip()) * 7
        date_value = date.today() - timedelta(n_days_ago)
    elif 'months ago' in age or 'month ago' in age:
        n_days_ago = int(age.replace('months ago', '').replace('month ago', '').strip()) * 30
        date_value = date.today() - timedelta(n_days_ago)
    else:
        date_value = age

    return date_value

