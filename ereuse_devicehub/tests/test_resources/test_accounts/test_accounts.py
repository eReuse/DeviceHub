import copy

from assertpy import assert_that

from ereuse_devicehub.exceptions import WrongCredentials
from ereuse_devicehub.security.perms import ACCESS
from ereuse_devicehub.tests import TestStandard


class TestDevice(TestStandard):
    def test_create_account(self):
        # Note that the default account we use in tests is role Admin and has access to all databases
        base_account = self.get_fixture(self.ACCOUNTS, 'account')
        base_account['databases'] = {
            self.db1: ACCESS,
            self.db2: ACCESS
        }

        # Admins can post accounts
        self.post_201(self.ACCOUNTS, base_account)
        user, status = self._post('login', base_account)
        self.assert200(status)

        # But employees cannot
        other_account = copy.deepcopy(base_account)
        other_account['email'] = 'x@x.com'
        response, status = self._post(self.ACCOUNTS, other_account, token=user['token'])
        self.assert422(status)
        assert_that(response['_issues']['databases'][0]).contains('ForbiddenToWrite')

        # Admins can create accounts to all databases
        # To check it let's create first an admin with only access to db1:
        admin = self.get_fixture(self.ACCOUNTS, 'admin')
        admin['databases'] = {self.db1: ACCESS}
        self.post_201(self.ACCOUNTS, admin)
        response, status = self._post('login', admin)
        self.assert200(status)
        manager_token = response['token']

        # And now let's create an account
        self.post_201(self.ACCOUNTS, other_account, token=manager_token)

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
