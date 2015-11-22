import json

from eve.tests import TestMinimal
from flask.ext.pymongo import MongoClient


class TestBase(TestMinimal):
    def setUp(self, settings_file=None, url_converters=None):
        from app.app import app

        app.config['MONGO_DBNAME'] = 'DeviceHubTest'
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
        self.db = self.connection[self.MONGO_DBNAME]
        self.connection.drop_database(self.MONGO_DBNAME)
        self.create_dummy_user()

    def create_dummy_user(self):
        self.db.accounts.insert(
            {'email': "a@a.a", 'password': "1234", 'role': 'superuser', 'token': 'NOFATDNNUB'}
        )

    def get(self, resource, query='', item=None):
        if resource in self.domain:
            resource = self.domain[resource]['url']
        if item:
            request = '/%s/%s%s' % (resource, item, query)
        else:
            request = '/%s%s' % (resource, query)
        r = self.test_client.get(request, environ_base={'HTTP_AUTHORIZATION': 'Basic ' + self.token})
        return self.parse_response(r)

    def post(self, url, data, headers=None, content_type='application/json'):
        if headers is None:
            headers = []
        return super(TestBase, self).post(url, data, headers + [self.auth_header], content_type)

    def patch(self, url, data, headers=None):
        if headers is None:
            headers = []
        return super(TestBase, self).patch(url, data, headers + [self.auth_header])

    def delete(self, url, headers=None):
        if headers is None:
            headers = []
        return super(TestBase, self).delete(url, headers + [self.auth_header])

    def _login(self) -> str:
        return super(TestBase, self).post('/login', {"email": "a@a.a", "password": "1234"})[0]['token']


class TestStandard(TestBase):
    def get_json_from_file(self, filename: str) -> dict:
        with open(filename) as data_file:
            return json.load(data_file)

    def isType(self,type:str,item:dict):
        return item['@type'] == type

    def assertType(self, type: str, item: dict):
        self.assertEqual(type, item['@type'])

    def assertLen(self, list: list, length: int):
        self.assertEqual(len(list), length)

