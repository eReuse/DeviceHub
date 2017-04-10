import argparse
import json

import requests
from bs4 import BeautifulSoup
from pydash import is_empty
from pydash import py_
from requests import HTTPError


class ManufacturersGetter:
    """
    Generates a JSON with a list of computer and mobile related manufacturers extracted from Wikipedia.

    To execute this you need the package BeautifoulSoup4 (just *pip install beautifulsoup4* it).
    """
    BASE_URL = 'https://en.wikipedia.org'
    PARAMS = (
        {
            'url': '/wiki/List_of_computer_hardware_manufacturers',
            'class': 'columns',
            'id': 'mw-content-text'
        },
        {
            'url': '/wiki/List_of_computer_system_manufacturers',
            'class': 'columns',
            'id': 'mw-content-text'
        },
        {
            'url': '/wiki/Category:Mobile_phone_manufacturers',
            'class': 'mw-category-group',
            'id': 'mw-pages'
        }
    )

    def execute(self, file_name: str = 'manufacturers.json'):
        """Executes *self.get()* and saves the list in a JSON file."""
        manufacturers = self.get()
        with open(file_name, 'w') as file:
            json.dump(manufacturers, file)

    def get(self) -> list:
        """
        Generates an unique and ordered list of canonical names of manufacturers obtained from different sources in
        Wikipedia.
        """
        print('Manufacturers:')
        urls = [self._manufacturers_url(self._get_page(p['url']), p['class'], p['id']) for p in self.PARAMS]
        return py_(urls).flatten().uniq().map_(lambda x: self._request(x['href'])) \
            .filter_(lambda x: not is_empty(x)).uniq().sort().value()

    def _get_page(self, url: str) -> BeautifulSoup:
        """Givern an URL, fetches the page and returns a beautifoulsoup page element."""
        r = requests.get(self.BASE_URL + url)
        r.raise_for_status()
        return BeautifulSoup(r.text, 'lxml')

    def _request(self, uri):
        """Obtains the canonical manufacturer name from a given URL, using Wikipedia's intelligence."""
        try:
            page = self._get_page(uri)
            manufacturer = page.find('title').get_text().replace(' - Wikipedia', '')
            print(manufacturer)
            return manufacturer
        except HTTPError:
            return None  # It will be erased later todo I do not like returning None, it should be an exception

    @staticmethod
    def _manufacturers_url(page: BeautifulSoup, class_: str, id_: str) -> list:
        """Finds the manufacturers' URL given a Wikipedia structured page."""
        containers = page.find(id=id_).find_all(class_=class_)
        return py_(containers).map_(lambda x: x.find_all('li')).flatten().map_(lambda x: x.a) \
            .remove(lambda x: not (is_empty(x) or 'index.php' in x or 'List of' in x)).value()


if __name__ == '__main__':
    desc = 'Generates a JSON with a list of computer and mobile related manufacturers extracted from Wikipedia.' \
           ' Internet required ofc.'
    epilog = 'Minimum example: python get_manufacturers.py'
    parser = argparse.ArgumentParser(description=desc, epilog=epilog)
    parser.parse_args()
    ManufacturersGetter().execute()
