import os

import requests

from ereuse_devicehub.default_settings import GRD_DOMAIN
from ereuse_devicehub.security.request_auth import Auth
from ereuse_devicehub.tests import TestStandard


class Dummy:
    def __init__(self, domain: str, database: str, email: str, password: str):
        self.domain = domain
        self.database = database
        self.email = email
        self.password = password
        self.auth = Auth(self.domain, self.email, self.password)

    def _execute(self):
        response = requests.get('{}/api/places'.format(GRD_DOMAIN), auth=GrdAuth())
        response.raise_for_status()
        places = response.json()['results']
        for place in places:
            place['type'] = 'CollectionPoint'
            place['@type'] = 'Place'
            del place['url']
            response = requests.post('{}/{}/{}'.format(self.domain, self.database, 'places'), json=place,
                                     auth=self.auth)
            response.raise_for_status()

    def _execute2(self):
        computers_id = []
        for device in self.get_devices_from_files():
            r = requests.post('{}/{}/{}'.format(self.domain, self.database, 'snapshot'), json=device, auth=self.auth)
            r.raise_for_status()
            computers_id.append(r.json()['_id'])

    @staticmethod
    def get_devices_from_files():
        this_directory = os.path.dirname(os.path.realpath(__file__))
        file_directory = os.path.join(this_directory, '..', 'test_events', 'test_snapshot', 'resources', '2015-12-09')
        for filename in os.listdir(file_directory):
            if 'json' in filename:
                yield TestStandard.get_json_from_file(filename, file_directory)
