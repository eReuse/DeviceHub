import json
import os
from pprint import pprint

from bson import ObjectId
from eve.io.mongo import MongoJSONEncoder
from eve.methods.common import parse

from eve.tests import TestMinimal
from flask.ext.pymongo import MongoClient
from passlib.handlers.sha2_crypt import sha256_crypt

from app.utils import get_resource_name
import json

class TestBase(TestMinimal):
    DEVICES = 'devices'
    EVENTS = 'events'
    PLACES = 'places'
    SNAPSHOT = 'snapshot'

    def setUp(self, settings_file=None, url_converters=None):
        import settings
        settings.MONGO_DBNAME = 'devicehubtest'
        settings.DATABASES = 'dht1', 'dht2'
        settings.DHT1_DBNAME = self.FIRST_DB = 'dth_1'
        settings.DHT2_DBNAME = self.SECOND_DB = 'dht_2'

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
        self.connection.drop_database(self.MONGO_DBNAME)
        self.db = self.connection[self.MONGO_DBNAME]
        self.create_dummy_user()

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

    def dropDB(self):
        self.connection = MongoClient(self.MONGO_HOST, self.MONGO_PORT)
        self.connection.drop_database(self.FIRST_DB)
        self.connection.drop_database(self.SECOND_DB)
        self.connection.drop_database(self.MONGO_DBNAME)
        self.connection.close()

    def full(self, resourceName: str, resource: dict or str or ObjectId) -> dict:
        return resource if type(resource) is dict else self.get(resourceName, '', str(resource))[0]

    def select_database(self, url):
        if 'accounts' in url:
            return ''
        else:
            return self.app.config['DATABASES'][0]

    def get(self, resource, query='', item=None):
        if resource in self.domain:
            resource = self.domain[resource]['url']
        if item:
            request = '/%s/%s%s' % (resource, item, query)
        else:
            request = '/%s%s' % (resource, query)
        r = self.test_client.get(self.select_database(resource) + request, environ_base={'HTTP_AUTHORIZATION': 'Basic ' + self.token})
        return self.parse_response(r)

    def post(self, url, data, headers=None, content_type='application/json'):
        if headers is None:
            headers = []
        return super(TestBase, self).post(self.select_database(url) + '/' + url, data, headers + [self.auth_header], content_type)

    def patch(self, url, data, headers=None):
        if headers is None:
            headers = []
        return super(TestBase, self).patch(self.select_database(url) + '/' + url, data, headers + [self.auth_header])

    def delete(self, url, headers=None):
        if headers is None:
            headers = []
        return super(TestBase, self).delete(self.select_database(url) + '/' + url, headers + [self.auth_header])

    def _login(self) -> str:
        return super(TestBase, self).post('/login', {"email": "a@a.a", "password": "1234"})[0]['token']


class TestStandard(TestBase):
    def get_json_from_file(self, filename: str, directory: str=None) -> dict:
        """

        :type filename: str
        :param directory: Optionall. Directory to get the file from. If nothing, it is taken from the actual directory.
        :return:
        """
        if directory is None:
            directory = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.abspath(os.path.join(directory, filename))) as data_file:
            value = json.load(data_file)
        with self.app.app_context():
            event = parse(value, get_resource_name(value['@type']))
            if 'components' in event:
                for device in event['components'] + [event['device']]:
                    device.update(parse(device, get_resource_name(device['@type'])))
            return event

    def isType(self, type:str, item:dict):
        return item['@type'] == type

    def assertType(self, type: str, item: dict):
        self.assertEqual(type, item['@type'])

    def assertLen(self, list: list, length: int):
        self.assertEqual(len(list), length)

    def get_fixture(self, resource_name, file_name):
        return self.get_json_from_file('fixtures/{}/{}.json'.format(resource_name, file_name))

    def post_fixture(self, resouce_name, file_name):
        return self.post_and_check(resouce_name, self.get_fixture(resouce_name, file_name))

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

