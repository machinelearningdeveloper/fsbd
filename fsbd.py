from configparser import ConfigParser
from io import BytesIO

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

res = requests.get(list_url)

f = BytesIO(res.content)

df = pd.read_excel(f)

df.to_excel(book_list_path)

def get_subject(book, subject_column):
    return book[subject_column].values[0]

book = df[df[book_url_column] == example_book_url]
book_subject = get_subject(book, book_subject_column)
print(book_subject)
