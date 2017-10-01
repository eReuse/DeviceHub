from assertpy import assert_that
from passlib.handlers.sha2_crypt import sha256_crypt

from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.security.perms import ACCESS, READ
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
                '@type': 'Account'
            }
        )
        self.account2 = self.login('b@b.b', '1234')
        self.token2 = self.account2['token']

    def test_reserve_in_shared_group(self):
        """Shares a group to a second user, and this second user reserves some inner devices, notifying the owner."""
        # Account is owner and performs share, and account2 will perform reserve
        # Create a lot and share it to account2
        lot = self.get_fixture(self.LOTS, 'lot')
        lot['children'] = {'devices': self.devices_id}
        lot['perms'] = [{'account': self.account2['_id'], 'perm': READ}]
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
