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

res = requests.get(list_url)

f = BytesIO(res.content)

df = pd.read_excel(f)

df.to_excel(book_list_path)
