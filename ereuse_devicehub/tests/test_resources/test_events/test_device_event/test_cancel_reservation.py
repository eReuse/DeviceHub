from assertpy import assert_that

from ereuse_devicehub.resources.event.device.cancel_reservation.settings import CancelReservation
from ereuse_devicehub.resources.event.device.sell.settings import Sell
from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent


class TestCancelReservation(TestDeviceEvent):
    def test_cancel_reservation(self):
        """Tests performing Cancel Reservation to a reserve."""
        reserve = {'@type': 'devices:Reserve', 'devices': self.devices_id}
        reserve = self.post_201(self.DEVICE_EVENT_RESERVE, reserve)
        reserve = self.get_200(self.EVENTS, item=reserve['_id'])

        cancel_reservation = {'@type': CancelReservation.type_name, 'reserve': reserve['_id']}
        with self.app.mail.record_messages() as outbox:
            cancel_reservation = self.post_201(self.DEVICE_EVENT_CANCEL_RESERVATION, cancel_reservation)
            cancel_reservation = self.get_200(self.EVENTS, item=cancel_reservation['_id'])
            assert_that(cancel_reservation).has_reserve(reserve['_id'])
            assert_that(cancel_reservation).has_for(reserve['for'])
            assert_that(cancel_reservation).has_notify(reserve['notify'])
            assert_that(outbox).is_length(2)
            assert_that(outbox[0]).has_recipients([self.account['email']])

    def test_cancel_reservation_without_reservation(self):
        """
        Tests the inability to cancel a non-existing reservation,
        double canceling a reservation or cancelling a succeeded (aka sold) reservation.
        """
        # 1 - Cancel a non-existing reservation
        #######################################
        cancel_reservation = {'@type': CancelReservation.type_name}
        response, status = self.post(self.DEVICE_EVENT_CANCEL_RESERVATION, data=cancel_reservation)
        assert_that(response).has__issues({'reserve': ['required field']})
        self.assert422(status)

        # 1 - Cancel a reservation that was sold before
        ###############################################
        # Note that this is the same for a Sell; it can't be performed if the reservation was cancelled.
        reserve = {'@type': 'devices:Reserve', 'devices': self.devices_id}
        reserve = self.post_201(self.DEVICE_EVENT_RESERVE, reserve)
        reserve = self.get_200(self.EVENTS, item=reserve['_id'])

        sell = {'@type': Sell.type_name, 'reserve': reserve['_id']}
        self.post_201(self.DEVICE_EVENT_SELL, data=sell)
        cancel_reservation = {'@type': CancelReservation.type_name, 'reserve': reserve['_id']}
        response, status = self.post(self.DEVICE_EVENT_CANCEL_RESERVATION, data=cancel_reservation)
        assert_that(response['_issues']['reserve'][0]).contains('NotUnique')
        self.assert422(status)
