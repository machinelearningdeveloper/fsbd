from configparser import ConfigParser
from io import BytesIO
import os
import os.path
import re
from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup
import pandas as pd
import requests

config = ConfigParser()

config.read('config.ini')
list_url = config['urls']['list_url']
example_book_url = config['urls']['example_book_url']
book_url_column = config['columns']['book_url_column']
book_list_path = config['paths']['book_list_path']
downloads_base_dir = config['paths']['downloads_base_dir']
book_subject_column = config['columns']['book_subject_column']
book_title_column = config['columns']['book_title_column']

res = requests.get(list_url)

f = BytesIO(res.content)

df = pd.read_excel(f)

df.to_excel(book_list_path)

def get_value(book, col):
    value = book[col].values
    assert len(value) == 1, "too many values"
    return value[0]

def get_subject(book, subject_column):
    return get_value(book, subject_column)

def get_title(book, title_column):
    return get_value(book, title_column)

def get_url(book, url_column):
    return get_value(book, url_column)

def get_page(url):
    res = None
    retries = 0
    while (not res or res.status_code != 200) and retries < 3:
        res = requests.get(url)
    if not res or res.status_code != 200:
        raise ValueError(f'unable to download content at url: {url}')
    return res.content.decode()

def normalize(txt):
    return re.sub(
        r'[^a-z0-9.]+',
        '_',
        txt.replace("'", ''),
        flags=re.IGNORECASE).strip('_').lower()

def mkdir(basedir, subdir):
    try:
        path = os.path.join(basedir, subdir)
        os.mkdir(path)
    except FileExistsError:
        pass

book = df[df[book_url_column] == example_book_url]
subject = get_subject(book, book_subject_column)
mkdir(downloads_base_dir, normalize(subject))

title = get_title(book, book_title_column)

book_url = get_url(book, book_url_column)

res = requests.get(book_url)
book_url_parsed = urlparse(res.url)
page = get_page(book_url)
soup = BeautifulSoup(page, 'html.parser')
pdf_url_rel = soup.find('a', class_='test-bookpdf-link')['href']
pdf_url_abs = urlunparse(
    (book_url_parsed.scheme,
    book_url_parsed.netloc,
    pdf_url_rel,
    book_url_parsed.params,
    book_url_parsed.query,
    book_url_parsed.fragment))
pdf = requests.get(pdf_url_abs)
