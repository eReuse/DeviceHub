import copy
import os
from pprint import pprint

import bson
from bson import ObjectId
from eve.io.mongo import MongoJSONEncoder
from eve.methods.common import parse

from eve.tests import TestMinimal
from flask.ext.pymongo import MongoClient
from passlib.handlers.sha2_crypt import sha256_crypt

from app.utils import Naming
import simplejson as json


class TestBase(TestMinimal):
    DEVICES = 'devices'
    EVENTS = 'events'
    PLACES = 'places'
    SNAPSHOT = 'snapshot'

    def setUp(self, settings_file=None, url_converters=None):
        import settings
        settings.MONGO_DBNAME = 'devicehubtest'
        settings.DATABASES = 'dht1', 'dht2'
        settings.DHT1_DBNAME = self.FIRST_DB = 'dht_1'
        settings.DHT2_DBNAME = self.SECOND_DB = 'dht_2'
        settings.GRD_DEBUG = True  # We do not want to actually fulfill GRD

        from app.app import app
        self.MONGO_DBNAME = app.config['MONGO_DBNAME']
        self.MONGO_HOST = app.config['MONGO_HOST']
        self.MONGO_PORT = app.config['MONGO_PORT']
        self.DATABASES = app.config['DATABASES']
        self.app = app

        self.connection = None
        self.known_resource_count = 101
        self.setupDB()

        self.test_client = self.app.test_client()
        self.domain = self.app.config['DOMAIN']

        self.token = self._login()
        self.auth_header = ('authorization', 'Basic ' + self.token)

    def setupDB(self):
        self.connection = MongoClient(self.MONGO_HOST, self.MONGO_PORT)
        self.db = self.connection[self.MONGO_DBNAME]
        self.drop_databases()
        self.create_dummy_user()
        # When executing many tests, it seems that the cache of pymongo has not been emptied
        # And the existance of the cache is used to know if it has benn called init_app, which has not
        # So we need to call init_app from here
        self.app.data.init_app(self.app)
        # We won't be able to close connection without this (we do not use media)
        self.app.media = {}

    def create_dummy_user(self):
        self.db.accounts.insert(
            {
                'email': "a@a.a",
                'password': sha256_crypt.encrypt('1234'),
                'role': 'superuser',
                'token': 'NOFATDNNUB',
                'databases': self.app.config['DATABASES'],
                'defaultDatabase': self.app.config['DATABASES'][0],
                '@type': 'Account'
            }
        )

    def drop_databases(self):
        self.connection.drop_database(self.MONGO_DBNAME)
        self.connection.drop_database(self.FIRST_DB)
        self.connection.drop_database(self.SECOND_DB)

    def dropDB(self):
        self.drop_databases()
        self.connection.close()

    def full(self, resourceName: str, resource: dict or str or ObjectId) -> dict:
        return resource if type(resource) is dict else self.get(resourceName, '', str(resource))[0]

    def select_database(self, url):
        if 'accounts' in url:
            return ''
        else:
            return self.app.config['DATABASES'][0]

    def get(self, resource, query='', item=None, authorize=True):
        if resource in self.domain:
            resource = self.domain[resource]['url']
        if item:
            request = '/%s/%s%s' % (resource, item, query)
        else:
            request = '/%s%s' % (resource, query)
        environ_base = {'HTTP_AUTHORIZATION': 'Basic ' + self.token} if authorize else {}
        r = self.test_client.get(self.select_database(resource) + request, environ_base=environ_base)
        return self.parse_response(r)

    def post(self, url, data, headers=None, content_type='application/json'):
        full_url = self.select_database(url) + '/' + url
        if headers is None:
            headers = []
        full_headers = headers + [self.auth_header]
        if type(data) is str:
            # todo this is part of super.post, the only modification is that it does not json.dumps()
            full_headers.append(('Content-Type', content_type))
            r = self.test_client.post(full_url, data=data, headers=full_headers)
            return self.parse_response(r)
        else:
            return super(TestBase, self).post(full_url, data, full_headers, content_type)

    def patch(self, url, data, headers=None):
        if headers is None:
            headers = []
        return super(TestBase, self).patch(self.select_database(url) + '/' + url, data, headers + [self.auth_header])

    def put(self, url, data, headers=None):
        if headers is None:
            headers = []
        return super(TestBase, self).put(self.select_database(url) + '/' + url, data, headers + [self.auth_header])

    def delete(self, url, headers=None):
        if headers is None:
            headers = []
        return super(TestBase, self).delete(self.select_database(url) + '/' + url, headers + [self.auth_header])

    def _login(self) -> str:
        return super(TestBase, self).post('/login', {"email": "a@a.a", "password": "1234"})[0]['token']


class TestStandard(TestBase):
    @staticmethod
    def get_json_from_file(filename: str, directory: str=None, parse_json=True) -> dict:
        """

        :type filename: str
        :param directory: Optionall. Directory to get the file from. If nothing, it is taken from the actual directory.
        :return:
        """
        if directory is None:
            directory = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.abspath(os.path.join(directory, filename))) as data_file:
            value = json.load(data_file) if parse_json else data_file.read()
        return value

    def parse_event(self, event):
        with self.app.app_context():
            event = parse(event, Naming.resource(event['@type']))
            if 'components' in event:
                for device in event['components'] + [event['device']]:
                    device.update(self.parse_device(device))
            return event

    def parse_device(self, device):
        """
        Parses the device using the standard way of parsing input data, using the settings of DeviceHub.

        This is needed when comparing a fixture with the device it represents, when this comparison happens
        inside with ... app_context()
        :param device:
        :return:
        """
        with self.app.app_context():
            return parse(copy.deepcopy(device), Naming.resource(device['@type']))

    def isType(self, type:str, item:dict):
        return item['@type'] == type

    def assertType(self, type: str, item: dict):
        self.assertEqual(type, item['@type'])

    def assertLen(self, list: list, length: int):
        self.assertEqual(len(list), length)

    def get_fixture(self, resource_name, file_name, parse_json=True):
        return self.get_json_from_file('fixtures/{}/{}.json'.format(resource_name, file_name), None, parse_json)

    def post_fixture(self, resource_name, url, file_name):
        return self.post_and_check(url, self.get_fixture(resource_name, file_name))

    def get_first(self, resource_name):
        return self.get_n(resource_name, 0)

    def get_n(self, resource_name, num):
        resources = self.get(resource_name)
        return resources[0]['_items'][num]

    def get_list(self, resource_name: str, identifiers: list):
        return [self.get(resource_name, '', identifier)[0] for identifier in identifiers]

    def post_and_check(self, url, payload):
        response, status_code = self.post(url, payload)
        try:
            self.assert201(status_code)
        except AssertionError as e:
            pprint(response)
            pprint(payload)
            e.message = response
            raise e
        return response

    def patch_and_check(self, url, payload):
        response, status_code = self.patch(url, payload)
        self.assert200(status_code)
        return response

    def put_and_check(self, url, payload):
        response, status_code = self.put(url, payload)
        self.assert200(status_code)
        return response

    def delete_and_check(self, url):
        response, status_code = self.delete(url)
        self.assert200(status_code)
        return response

    def get_fixtures_computers(self) -> list:
        """
        Snapshots four computers in the database, and returns a list with their identifiers.

        One computer has no HID, and it has been Snapshotted with the option 'force_creation' to True.
        :return:
        """
        vaio = self.post_fixture(self.SNAPSHOT, '{}/{}'.format(self.EVENTS, self.SNAPSHOT), 'vaio')
        vostro = self.post_fixture(self.SNAPSHOT, '{}/{}'.format(self.EVENTS, self.SNAPSHOT), 'vostro')
        xps13 = self.post_fixture(self.SNAPSHOT, '{}/{}'.format(self.EVENTS, self.SNAPSHOT), 'xps13')
        mounted = self.get_fixture(self.SNAPSHOT, 'mounted')
        mounted['device']['forceCreation'] = True
        mounted = self.post_and_check('{}/{}'.format(self.EVENTS, self.SNAPSHOT), mounted)
        return [self.get(self.EVENTS, '', event['events'][0])[0]['device'] for event in [vaio, vostro, xps13, mounted]]

    def device_and_place_contain_each_other(self, device_id: str, place_id: str) -> list:
        """
        Checks that the materialization of device-place is correct. This is, the place has a reference to a device
        and the device has a reference to a place. If the device has components, this checks the same for the components.
        :param device_id:
        :param place_id:
        :return:
        """
        place, _ = self.get(self.PLACES, '', place_id)
        self.assertIn('devices', place)
        self.assertIn(device_id, place['devices'])
        device, _ = self.get(self.DEVICES, '', device_id)
        self.assertIn('place', device)
        self.assertIn(place_id, device['place'])
        if 'components' in device:
            for component_id in device['components']:
                component, _ = self.get(self.DEVICES, '', component_id)
                self.assertIn('place', component)
                self.assertIn(place_id, component['place'])