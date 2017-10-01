from assertpy import assert_that

from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent


class TestCancelReservation(TestDeviceEvent):
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
