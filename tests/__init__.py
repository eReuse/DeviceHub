import json
import os
from eve.methods.common import parse

from eve.tests import TestMinimal
from flask.ext.pymongo import MongoClient
from passlib.handlers.sha2_crypt import sha256_crypt

from app.utils import get_resource_name

import importlib

class TestBase(TestMinimal):
    def setUp(self, settings_file=None, url_converters=None):
        from app.app import app
        # app.config['MONGO_DBNAME'] = 'DeviceHubTest'
        # app.config['DATABASES'] = ['dht1', 'dht2']
        # app.config['DHT1_DBNAME'] = 'dht_1'
        # app.config['DHT2_DBNAME'] = 'dht_2'
        self.MONGO_DBNAME = app.config['MONGO_DBNAME']
        self.MONGO_HOST = app.config['MONGO_HOST']
        self.MONGO_PORT = app.config['MONGO_PORT']
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
                'defaultDatabase': self.app.config['DATABASES'][0]
            }
        )

    def dropDB(self):
        self.connection = MongoClient(self.MONGO_HOST, self.MONGO_PORT)
        self.connection.drop_database('dh_db1')
        self.connection.drop_database('dh_db2')
        self.connection.drop_database('dh__accounts')
        self.connection.close()

    def get(self, resource, query='', item=None):
        if resource in self.domain:
            resource = self.domain[resource]['url']
        if item:
            request = '/%s/%s%s' % (resource, item, query)
        else:
            request = '/%s%s' % (resource, query)
        r = self.test_client.get(self.app.config['DATABASES'][0] + request, environ_base={'HTTP_AUTHORIZATION': 'Basic ' + self.token})
        return self.parse_response(r)

    def post(self, url, data, headers=None, content_type='application/json'):
        if headers is None:
            headers = []
        return super(TestBase, self).post(self.app.config['DATABASES'][0] + '/' + url, data, headers + [self.auth_header], content_type)

    def patch(self, url, data, headers=None):
        if headers is None:
            headers = []
        return super(TestBase, self).patch(self.app.config['DATABASES'][0] + '/' + url, data, headers + [self.auth_header])

    def delete(self, url, headers=None):
        if headers is None:
            headers = []
        return super(TestBase, self).delete(self.app.config['DATABASES'][0] + '/' + url, headers + [self.auth_header])

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


    def isType(self,type:str,item:dict):
        return item['@type'] == type

    def assertType(self, type: str, item: dict):
        self.assertEqual(type, item['@type'])

    def assertLen(self, list: list, length: int):
        self.assertEqual(len(list), length)

