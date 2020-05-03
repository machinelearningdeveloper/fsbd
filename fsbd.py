from configparser import ConfigParser

config = ConfigParser()

config.read('config.ini')
list_url = config['urls']['list_url']
example_book_url = config['urls']['example_book_url']
book_url_column = config['columns']['book_url_column']
