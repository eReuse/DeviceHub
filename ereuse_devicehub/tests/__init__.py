import contextlib
import copy
import os
from urllib.parse import urlencode

from assertpy import assert_that
from bson.objectid import ObjectId
from eve.methods.common import parse
from eve.tests import TestMinimal
from flask import json
from flask.ext.pymongo import MongoClient

from ereuse_devicehub import utils
from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.flaskapp import DeviceHub
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.submitter.grd_submitter.grd_submitter import GRDSubmitter
from ereuse_devicehub.resources.submitter.submitter_caller import SubmitterCaller
from ereuse_devicehub.utils import Naming


class TestBase(TestMinimal):
    DEVICES = 'devices'
    DEVICE_EVENT = 'events/devices'
    EVENTS = 'events'
    PLACES = 'places'
    SNAPSHOT = 'snapshot'
    ACCOUNTS = 'accounts'
    GROUPS = 'groups'
    LOTS = 'lots'
    PACKAGES = 'packages'

    def setUp(self, settings_file=None, url_converters=None):
        # noinspection PyUnresolvedReferences
        from ereuse_devicehub import default_settings as settings
        self.set_settings(settings)
        self.app = DeviceHub()
        self.prepare()

    @staticmethod
    def set_settings(settings):
        settings.MONGO_DBNAME = 'devicehubtest'
        settings.DATABASES = 'dht1', 'dht2'  # Some tests use 2 databases
        settings.DHT1_DBNAME = 'dht1_'
        settings.DHT2_DBNAME = 'dht2_'
        settings.GRD_DEBUG = True  # We do not want to actually fulfill GRD
        settings.APP_NAME = 'DeviceHub'
        settings.DEBUG = True
        settings.TESTING = True
        settings.LOG = True
        settings.GRD = False
        settings.AGENT_ACCOUNTS = {
            'self': ('self@ereuse.org', '12345')
        }
        settings.MAXMIND_ACCOUNT = {
            'user': 1,
            'license key': 'license-key'
        }

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

        self.db2 = self.app.config['DATABASES'][1]  # 'dht2'
        self.db1 = self.app.config['DATABASES'][0]  # 'dht1'

    def setupDB(self):
        self.connection = MongoClient(self.MONGO_HOST, self.MONGO_PORT)
        self.db = self.connection[self.MONGO_DBNAME]
        self.drop_databases()
        self.create_dummy_user()
        self.create_self_machine_account()
        if self.app.config.get('GRD', False):
            # We call the method again as we have erased the DB
            self.app.grd_submitter_caller = SubmitterCaller(self.app, GRDSubmitter)
        # self.app.grd_submitter_caller.token = self.app.grd_submitter_caller.prepare_user(self.app)
        # self.app.grd_submitter_caller.process = None

    def create_dummy_user(self):
        self.db.accounts.insert_one(
            {
                'email': "a@a.a",
                'password': AccountDomain.encrypt_password('1234'),
                'role': 'admin',
                'token': 'NOFATDNNUB',
                'databases': self.app.config['DATABASES'],
                'defaultDatabase': self.app.config['DATABASES'][0],
                '@type': 'Account'
            }
        )
        self.account = self.db.accounts.find_one({'email': 'a@a.a'})

    def create_self_machine_account(self):
        email, password = self.app.config['AGENT_ACCOUNTS']['self']
        self.db.accounts.insert_one(
            {
                'role': 'superuser',
                'token': 'QYADFBPNZZDFJEWAFGGF',
                'databases': self.app.config['DATABASES'],
                '@type': 'Account',
                'email': email,
                'password': AccountDomain.encrypt_password(password)
            }
        )

    def tearDown(self):
        self.drop_databases()
        if hasattr(self.app, 'grd_submitter_caller'):
            # We terminate the child process
            del self.app.grd_submitter_caller
        del self.app


    def drop_databases(self):
        self.connection.drop_database(self.MONGO_DBNAME)
        for database in self.DATABASES:
            self.connection.drop_database(self.app.config[database.upper().replace('-', '') + '_DBNAME'])

    def full(self, resource_name: str, resource: dict or str or ObjectId) -> dict:
        return resource if type(resource) is dict else self.get(resource_name, '', str(resource))[0]

    def select_database(self, url):
        if 'accounts' in url:
            return ''
        else:
            return self.app.config['DATABASES'][0]

    def get(self, resource, query='', item=None, authorize=True, database=None, params=None, embedded=None):
        if embedded:
            params = params or {}
            params['embedded'] = json.dumps(embedded)
        if params:
            query += ('&' if '?' in query else '?') + urlencode(params, True)
        if resource in self.domain:
            resource = self.domain[resource]['url']
        if item:
            request = '/%s/%s%s' % (resource, item, query)
        else:
            request = '/%s%s' % (resource, query)

        database = database or self.select_database(resource)
        return self._get(database + request, self.token if authorize else None)

    def _get(self, url, token=None, **kwargs):
        environ_base = {'HTTP_AUTHORIZATION': 'Basic ' + token} if token else {}
        environ_base.update(kwargs.pop('environ_base', {}))
        r = self.test_client.get(url, environ_base=environ_base, **kwargs)
        return self.parse_response(r)

    def post(self, url, data, headers=None, content_type='application/json'):
        full_url = self.select_database(url) + '/' + url
        headers = headers or []
        return self._post(full_url, data, self.token, headers, content_type)

    def _post(self, url, data, token: str=None, headers=None, content_type='application/json'):
        headers = headers or []
        if token:
            headers.append(('Authorization', 'Basic ' + token))
        if type(data) is str:
            headers.append(('Content-Type', content_type))
            r = self.test_client.post(url, data=data, headers=headers)
            return self.parse_response(r)
        return super(TestBase, self).post(url, data, headers, content_type)

    def patch(self, url, data, headers=None, item=None):
        headers = headers or []
        url = url + '/' + str(item) if item else url
        return self._patch(self.select_database(url) + '/' + url, data, self.token, headers)

    def _patch(self, url, data, token, headers=None):
        headers = headers or []
        headers.append(('authorization', 'Basic ' + token))
        return super(TestBase, self).patch(url, data, headers)

    def put(self, url, data, headers=None):
        headers = headers or []
        return super(TestBase, self).put(self.select_database(url) + '/' + url, data, headers + [self.auth_header])

    def delete(self, url, headers=None, item=None):
        headers = headers or []
        if item:
            url = url + '/' + item
        return super(TestBase, self).delete(self.select_database(url) + '/' + url, headers + [self.auth_header])

    def _login(self) -> str:
        return super(TestBase, self).post('/login', {"email": "a@a.a", "password": "1234"})[0]['token']

    def assert308(self, status):
        self.assertEqual(status, 308)


class TestStandard(TestBase):
    @staticmethod
    def get_json_from_file(filename: str, directory: str = None, parse_json=True, mode='r') -> dict:
        if directory is None:
            directory = os.path.dirname(os.path.realpath(__file__))
        return utils.get_json_from_file(filename, directory, parse_json, mode)

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
        with self._print_unsuccessful_request(url, response, status_code, payload):
            self.assert201(status_code)
        return response

    def patch_and_check(self, url, payload, item=None):
        response, status_code = self.patch(url, payload, item=item)
        with self._print_unsuccessful_request(url, response, status_code, payload):
            self.assert200(status_code)
        return response

    def put_and_check(self, url, payload):
        response, status_code = self.put(url, payload)
        with self._print_unsuccessful_request(url, response, status_code, payload):
            self.assert200(status_code)
        return response

    def delete_and_check(self, url, item=None):
        response, status_code = self.delete(url, item=item)
        with self._print_unsuccessful_request(url, response, status_code):
            self.assert204(status_code)
        return response

    def assert_error(self, response: dict, status_code: int, error_class: type(StandardError)):
        """Ensures that the response (a dict from a JSON) represents the *error_class*."""
        name = error_class.__name__
        if error_class.status_code != status_code or response['_error']['@type'] != name:
            raise AssertionError('Response error {} is not an instance of error {}.'.format(response, name))

    @contextlib.contextmanager
    def _print_unsuccessful_request(self, url, response, status_code, payload=None):
        try:
            yield
        except AssertionError:
            m = 'Unsuccessful request on {} (HTTP {}):\n'.format(url, status_code)
            if payload:
                m += 'Payload:\n{}\n'.format(payload)
            m += 'Response:\n{}'.format(response)
            raise AssertionError(m)

    def get_and_check(self, resource, query='', item=None, authorize=True, database=None, params=None, embedded=None):
        response, status_code = self.get(resource, query, item, authorize, database, params, embedded)
        try:
            self.assert200(status_code)
        except AssertionError:
            text = '{} when HTTP 200 expected, resource {} q {} item {} params {} embedded {}'
            raise AssertionError(text.format(status_code, resource, query, item, params, embedded))
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
        return [self.get_and_check(self.EVENTS, item=event['events'][0])['device'] for event in [vaio, vostro, xps13, mounted]]

    def devices_do_not_contain_places(self, device_id: str):
        """ The opposite of `device_and_place_contain_each_other`."""
        device = self.get_and_check(self.DEVICES, item=device_id)
        assert_that(device).does_not_contain('place')
        for component_id in device.get('components', []):
            component = self.get_and_check(self.DEVICES, item=component_id)
            assert_that(component).does_not_contain('place')

    def set_superuser(self):
        with self.app.app_context():
            AccountDomain.update_raw(self.account['_id'], {'$set': {'role': 'superuser'}})
