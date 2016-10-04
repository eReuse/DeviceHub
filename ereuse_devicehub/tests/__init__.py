import copy
import os
from pprint import pprint

import simplejson as json
from assertpy import assert_that
from bson.objectid import ObjectId
from ereuse_devicehub.flaskapp import DeviceHub
from ereuse_devicehub.resources.submitter.grd_submitter.grd_submitter import GRDSubmitter
from ereuse_devicehub.resources.submitter.submitter_caller import SubmitterCaller
from ereuse_devicehub.utils import Naming
from eve.methods.common import parse
from eve.tests import TestMinimal
from flask.ext.pymongo import MongoClient
from passlib.handlers.sha2_crypt import sha256_crypt


class TestBase(TestMinimal):
    DEVICES = 'devices'
    DEVICE_EVENT = 'events/devices'
    EVENTS = 'events'
    PLACES = 'places'
    SNAPSHOT = 'snapshot'
    ACCOUNTS = 'accounts'

    def setUp(self, settings_file=None, url_converters=None):
        from ereuse_devicehub import default_settings as settings
        self.set_settings(settings)
        self.app = DeviceHub()
        self.prepare()

    def set_settings(self, settings):
        settings.MONGO_DBNAME = 'devicehubtest'
        settings.DATABASES = 'dht1', 'dht2'
        settings.DHT1_DBNAME = 'dht1_'
        settings.DHT2_DBNAME = 'dht2_'
        settings.GRD_DEBUG = True  # We do not want to actually fulfill GRD
        settings.APP_NAME = 'DeviceHub'
        settings.DEBUG = True
        settings.TESTING = True
        settings.LOG = True
        settings.GRD = True
        settings.BASE_PATH_SHOWN_TO_GRD = 'https://www.example.com'

    def prepare(self):
        self.MONGO_DBNAME = self.app.config['MONGO_DBNAME']
        self.MONGO_HOST = self.app.config['MONGO_HOST']
        self.MONGO_PORT = self.app.config['MONGO_PORT']
        self.DATABASES = self.app.config['DATABASES']

        self.connection = None
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
        # We call the method again as we have erased the DB
        self.app.grd_submitter_caller = SubmitterCaller(self.app, GRDSubmitter)
        # self.app.grd_submitter_caller.token = self.app.grd_submitter_caller.prepare_user(self.app)
        # self.app.grd_submitter_caller.process = None

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
        self.account = self.db.accounts.find_one({'email': 'a@a.a'})

    def tearDown(self):
        self.dropDB()
        del self.app

    def drop_databases(self):
        self.connection.drop_database(self.MONGO_DBNAME)
        for database in self.app.config['DATABASES']:
            self.connection.drop_database(self.app.config[database.upper() + '_DBNAME'])

    def dropDB(self):
        self.drop_databases()
        self.connection.close()

    def full(self, resource_name: str, resource: dict or str or ObjectId) -> dict:
        return resource if type(resource) is dict else self.get(resource_name, '', str(resource))[0]

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

    def assert308(self, status):
        self.assertEqual(status, 308)


class TestStandard(TestBase):
    @staticmethod
    def get_json_from_file(filename: str, directory: str = None, parse_json=True, mode='r') -> dict:
        """

        :type filename: str
        :param directory: Optionall. Directory to get the file from. If nothing, it is taken from the actual directory.
        :return:
        """
        if directory is None:
            directory = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.abspath(os.path.join(directory, filename)), mode=mode) as data_file:
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

    @staticmethod
    def isType(t: str, item: dict):
        return item['@type'] == t

    def assertType(self, t: str, item: dict):
        self.assertEqual(t, item['@type'])

    def assertLen(self, list_to_assert: list, length: int):
        self.assertEqual(len(list_to_assert), length)

    def get_fixture(self, resource_name, file_name, parse_json=True, directory=None, extension='json', mode='r'):
        return self.get_json_from_file('fixtures/{}/{}.{}'.format(resource_name, file_name, extension), directory,
                                       parse_json, mode)

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
        self.assert204(status_code)
        return response

    def get_fixtures_computers(self) -> list:
        """
        Snapshots four computers in the database, and returns a list with their identifiers.

        One computer has no HID, and it has been Snapshotted with the option 'force_creation' to True.
        :return:
        """
        vaio = self.post_fixture(self.SNAPSHOT, '{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), 'vaio')
        vostro = self.post_fixture(self.SNAPSHOT, '{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), 'vostro')
        xps13 = self.post_fixture(self.SNAPSHOT, '{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), 'xps13')
        mounted = self.get_fixture(self.SNAPSHOT, 'mounted')
        mounted['device']['forceCreation'] = True
        mounted = self.post_and_check('{}/{}'.format(self.DEVICE_EVENT, self.SNAPSHOT), mounted)
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
        self.assertEqual(place_id, device['place'])
        for component_id in device.get('components', []):
            component, _ = self.get(self.DEVICES, '', component_id)
            self.assertIn('place', component)
            self.assertEqual(component['place'], place_id)

    def devices_do_not_contain_places(self, device_id: str) -> list:
        """ The opposite of `device_and_place_contain_each_other`."""
        device, _ = self.get(self.DEVICES, '', device_id)
        assert_that(device).does_not_contain('place')
        for component_id in device.get('components', []):
            component, _ = self.get(self.DEVICES, '', component_id)
            assert_that(component).does_not_contain('place')
