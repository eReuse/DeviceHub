import copy

from assertpy import assert_that

from ereuse_devicehub.exceptions import WrongCredentials
from ereuse_devicehub.tests import TestStandard


class TestDevice(TestStandard):
    @staticmethod
    def set_settings(settings):
        super(TestDevice, TestDevice).set_settings(settings)
        settings.DATABASES += 'dht3',  # We add a third database
        settings.DHT3_DBNAME = 'dht3_'

    def test_create_account(self):
        base_account = self.get_fixture(self.ACCOUNTS, 'account')
        # Superusers can post accounts
        self.post_and_check(self.ACCOUNTS, base_account)
        employee, status = self._post('login', base_account)
        self.assert200(status)
        # But employees cannot
        other_account = copy.deepcopy(base_account)
        other_account['email'] = 'x@x.com'
        response, status = self._post(self.ACCOUNTS, other_account, employee['token'])
        self.assert422(status)
        assert_that(response['_issues']['databases'][0]).contains('ForbiddenToWrite')
        # todo Admins can only create an account that is in a database they are in
        # other_account['databases'].append('dht3')
        # _, status = self.post(self.ACCOUNTS, other_account)
        # self.assert422(status)
        # del other_account['databases'][-1]
        # self.post_and_check(self.ACCOUNTS, other_account)

    def test_login(self):
        """Tests invalid logins"""
        # Normal login is performed for every test in a '_login' method in TestBase superclass
        # So there is no need to test it here again
        # Test Wrong credentials
        response, status = self._post('/login', {'email': 'a@a.a', 'password': 'wrong password'})
        self.assert_error(response, status, WrongCredentials)
        # No credentials at all
        _, status = self._post('/login', {})
        self.assert_error(response, status, WrongCredentials)


