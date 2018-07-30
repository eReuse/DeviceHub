import argparse
import json
from contextlib import suppress

import requests
from bs4 import BeautifulSoup
from pydash import find
from pydash import is_empty
from pydash import py_
from requests import HTTPError
from wikipedia import wikipedia

from ereuse_devicehub.resources.manufacturers import ManufacturerDomain
from ereuse_devicehub.utils import get_json_from_file


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
    VALUES_TO_REMOVE = 'Hewlett',
    # HP has many companies called the same and Wikpedia accounts for each of them, and HP Inc is the new name for
    # The old Hewlett-Packard
    PATHS_TO_REMOVE = 'index.php', 'List of'
    LOGO_AVOID = 'commons-logo', 'old'
    FILENAME = '_manufacturers.json'
    CUSTOM_MANUFACTURERS = {'Belinea', 'OKI Data Corporation', 'Vivitek', 'Yuraku'}
    """
    A list of manufacturer labels (names) 
    that are not in (or we can't take them from) Wikipedia,
    so we can add them too.
    """

    def execute(self, app):
        """
        Populates the database with the manufacturers. This method will try to locate a *_manufacturers.json* and
        populate from there. If the file does not exist it will fetch the data from Wikipedia (taking long time) and
        then saving it in the database and the *_manufacturers.json* file (think of it as a cache).
        :param app:
        :return:
        """
        with app.app_context():
            ManufacturerDomain.delete_all()
            try:
                for man in get_json_from_file(self.FILENAME, same_directory_as_file=__file__):
                    ManufacturerDomain.insert(man)
            except FileNotFoundError:
                m = []
                for manufacturer_name in self.get():
                    with suppress(Exception):
                        page = wikipedia.page(manufacturer_name, auto_suggest=False, redirect=False)
                        man = {
                            'label': manufacturer_name,
                            'url': page.url
                        }
                        with suppress(Exception):
                            man['logo'] = find(
                                page.images,
                                lambda x: 'logo' in x.lower() and not any(v in x.lower() for v in self.LOGO_AVOID)
                            )
                        m.append(man)
                        ManufacturerDomain.insert(man)
                with open(self.FILENAME, 'w') as fp:
                    json.dump(m, fp)
            for label in self.CUSTOM_MANUFACTURERS:
                ManufacturerDomain.insert({'label': label})

    def get(self) -> list:
        """
        Generates an unique and ordered list of canonical names of manufacturers obtained from different sources in
        Wikipedia.
        """
        print('Manufacturers:')
        urls = [self._manufacturers_url(self._get_page(p['url']), p['class'], p['id']) for p in self.PARAMS]
        return py_(urls).flatten().uniq().map_(lambda x: self._request(x['href'])) \
            .filter_(lambda x: not (is_empty(x) or any(v in x for v in self.VALUES_TO_REMOVE))).uniq().sort().value()

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

    @classmethod
    def _manufacturers_url(cls, page: BeautifulSoup, class_: str, id_: str) -> list:
        """Finds the manufacturers' URL given a Wikipedia structured page."""
        containers = page.find(id=id_).find_all(class_=class_)
        return py_(containers).map_(lambda x: x.find_all('li')).flatten().map_(lambda x: x.a). \
            remove(lambda x: not (is_empty(x) or any(v in x for v in cls.PATHS_TO_REMOVE))).value()


if __name__ == '__main__':
    desc = 'Generates a JSON with a list of computer and mobile related manufacturers extracted from Wikipedia.' \
           ' Internet required ofc.'
    epilog = 'Minimum example: python get_manufacturers.py'
    parser = argparse.ArgumentParser(description=desc, epilog=epilog)
    parser.parse_args()

    from ereuse_devicehub import DeviceHub

    app = DeviceHub()
    ManufacturersGetter().execute(app)
