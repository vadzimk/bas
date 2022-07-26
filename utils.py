import os
import re
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def make_soup(url, export_filename):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0'  # https://webbrowsertools.com/useragent/
    headers = {'User-Agent': user_agent}
    res = requests.get(url, headers)
    print(res.status_code, url)
    save_safe(res.text, export_filename)
    return BeautifulSoup(res.content, 'html.parser')


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
