from typing import List

from flask import current_app as app

from ereuse_devicehub.mails.mails import create_email
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.cancel_reservation.settings import CancelReservation
from ereuse_devicehub.resources.event.device.reserve.settings import Reserve
from ereuse_devicehub.utils import url_for_resource


def set_for_and_notify(cancel_reservations: List[dict]):
    """Copies the ``for`` and ``notify`` of the reservation this is cancelling"""
    for cancel_reservation in cancel_reservations:
        reserve = DeviceEventDomain.get_one(cancel_reservation['reserve'])
        cancel_reservation['for'] = reserve['for']
        cancel_reservation['notify'] = reserve['notify']


def notify(cancel_reservations: List[dict]):
    msgs = []
    for cancel_reservation in cancel_reservations:
        context = {
            'reserve_url': url_for_resource(Reserve.resource_name, cancel_reservation['reserve']),
            'cancel_reservation_url': url_for_resource(CancelReservation.resource_name, cancel_reservation['_id']),
            'for': AccountDomain.get_one(cancel_reservation['for'])
        }
        msgs.append(create_email('mails/cancel_reserve_for.html', context['for'], **context))
        for recipient in AccountDomain.get_in('_id', cancel_reservation['notify']):
            msgs.append(create_email('mails/cancel_reserve_notify.html', recipient, **context))
    # We send all emails with the same connection (+ speed)
    with app.mail.connect() as conn:
        for msg in msgs:
            conn.send(msg)


def materialize_cancel_in_reserve(cancel_reservations: List[dict]):
    """Materializes the field 'cancel' in reserve."""
    cancel_reservation = cancel_reservations[0]
    if 'reserve' in cancel_reservation:
        DeviceEventDomain.update_one_raw(cancel_reservation['reserve'], {'$set': {'cancel': cancel_reservation['_id']}})
