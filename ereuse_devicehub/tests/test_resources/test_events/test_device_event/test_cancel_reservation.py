from assertpy import assert_that
from passlib.handlers.sha2_crypt import sha256_crypt

from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.security.perms import ACCESS
from ereuse_devicehub.tests import TestBase
from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent


class TestCancelReservation(TestDeviceEvent):
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
        self.account2, _ = super(TestBase, self).post('/login', {'email': 'b@b.b', 'password': '1234'})
        self.token2 = self.account2['token']

    def test_cancel_reservation(self):
        """Tests performing Cancel Reservation to a reserve."""
        reserve = {'@type': 'devices:Reserve', 'devices': self.devices_id}
        reserve = self.post_201(self.DEVICE_EVENT_RESERVE, reserve)
        reserve = self.get_200(self.EVENTS, item=reserve['_id'])

        cancel_reservation = {'@type': 'devices:CancelReservation', 'reserve': reserve['_id']}
        with self.app.mail.record_messages() as outbox:
            cancel_reservation = self.post_201(self.DEVICE_EVENT_CANCEL_RESERVATION, cancel_reservation)
            cancel_reservation = self.get_200(self.EVENTS, item=cancel_reservation['_id'])
            assert_that(cancel_reservation).has_reserve(reserve['_id'])
            assert_that(cancel_reservation).has_for(reserve['for'])
            assert_that(cancel_reservation).has_notify(reserve['notify'])
            assert_that(outbox).is_length(2)
            assert_that(outbox[0]).has_recipients([self.account['email']])

    def test_cancel_reservation_without_reservation(self):
        """Tests the inability to cancel a non-existing reservation, or double canceling a reservation."""
        # todo
        pass
