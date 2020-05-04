from configparser import ConfigParser
from io import BytesIO
import os
import os.path
import re

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

def get_subject(book, subject_column):
    return book[subject_column].values[0]

def get_title(book, title_column):
    return book[title_column].values[0]

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
print(title)
