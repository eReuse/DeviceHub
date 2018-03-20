from json import dumps

from assertpy import assert_that
from passlib.handlers.sha2_crypt import sha256_crypt

from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.event.device.reserve.settings import Reserve
from ereuse_devicehub.security.perms import ACCESS, READ, ADMIN
from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent


class TestReserve(TestDeviceEvent):
    def setUp(self, settings_file=None, url_converters=None):
        super().setUp(settings_file, url_converters)
        self.db.accounts.insert_one(
            {
                'email': 'b@b.b',
                'password': sha256_crypt.hash('1234'),
                'role': Role.ADMIN,
                'token': 'TOKENB',
                'databases': {self.app.config['DATABASES'][1]: ACCESS},
                'defaultDatabase': self.app.config['DATABASES'][1],
                '@type': 'Account',
                'active': True
            }
        )
        self.account2 = self.login('b@b.b', '1234')
        self.token2 = self.account2['token']

    def test_reserve_in_shared_group(self):
        """
        Shares a group to a second user, and this second user reserves
        some inner devices, notifying the owner.
        """

        # Let's add an extra account (account3)
        # This account is not active so it does not receive any email
        self.db.accounts.insert_one(
            {
                'email': 'c@c.c',
                'password': sha256_crypt.hash('1234'),
                'role': Role.ADMIN,
                'token': 'TOKENC',
                'databases': {self.app.config['DATABASES'][0]: ADMIN},
                'defaultDatabase': self.app.config['DATABASES'][0],
                '@type': 'Account',
                'active': False
            }
        )
        # Account is owner and performs share, and account2 will perform reserve
        # Create a lot and share it to account2
        lot = self.get_fixture(self.LOTS, 'lot')
        lot['children'] = {'devices': self.devices_id}
        lot['perms'] = [
            {'account': self.account2['_id'], 'perm': READ}
        ]
        self.post_201(self.LOTS, lot)

        devices_to_reserve = self.devices_id[:2]

        reserve = {'@type': 'devices:Reserve', 'devices': devices_to_reserve}
        with self.app.mail.record_messages() as outbox:
            reserve = self.post_201(self.DEVICE_EVENT_RESERVE, reserve, token=self.token2)
            assert_that(reserve).has_for(self.account2['_id'])
            assert_that(reserve).has_notify([str(self.account['_id'])])
            assert_that(outbox).is_length(2)
            assert_that(outbox[0].recipients).is_equal_to(['b@b.b'])
            assert_that(outbox[0].html).contains('New reservation of devices')
            assert_that(outbox[1].recipients).is_equal_to(['a@a.a'])
            assert_that(outbox[1].html).contains('Your reservation')
        reserve = self.get_200(self.EVENTS, item=reserve['_id'], token=self.token2)
        assert_that(reserve).has_devices(devices_to_reserve)
        assert_that(reserve).has_for(self.account2['_id'])
        assert_that(reserve).has_notify([str(self.account['_id'])])

    def test_reserve_new_user(self):
        """Tests reserving where its 'to' is a new user. A difference is, for example, that no email is sent."""
        reserve = {'@type': Reserve.type_name, 'devices': self.devices_id, 'for': {'email': 'foo@bar.com'}}
        with self.app.mail.record_messages() as outbox:
            reserve = self.post_201(self.DEVICE_EVENT_RESERVE, reserve)
            account = self.get_200(self.ACCOUNTS, params={'where': dumps({'email': 'foo@bar.com'})})['_items'][0]
            assert_that(reserve).has_for(account['_id'])
            # The new created account is not active so no e-mail is sent to it
            assert_that(account['active']).is_false()
            assert_that(reserve).has_notify([str(self.account['_id'])])
            assert_that(outbox).is_length(1)
            assert_that(outbox[0]).has_recipients(['a@a.a'])

