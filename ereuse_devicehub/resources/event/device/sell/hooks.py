from typing import List

from flask import current_app as app

from ereuse_devicehub.mails.mails import create_email, suppressAndLogSendingException
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.reserve.settings import Reserve
from ereuse_devicehub.utils import url_for_resource


def set_to(sells: List[dict]):
    sell = sells[0]
    if 'reserve' in sell and 'to' not in sell:
        reserve = DeviceEventDomain.get_one(sell['reserve'])
        sell['to'] = reserve['for']


def notify(sells: List[dict]):
    """Sends an e-mail about the selling to the buyer, if any."""
    sell = sells[0]
    if 'to' in sell:
        to = AccountDomain.get_one(sell['to'])
        if to['active']:
            context = {
                'fields': (
                    {'path': '_id', 'name': 'ID in ' + AccountDomain.requested_database},
                    {'path': '@type', 'name': 'Type'},
                    {'path': 'type', 'name': 'Subtype'},
                    {'path': 'serialNumber', 'name': 'S/N'}
                ),
                'devices': DeviceDomain.get_in('_id', sell['devices']),
                'sell_url': url_for_resource(Reserve.resource_name, sell['_id']),
            }
            msg = create_email('mails/sell.html', to, **context)
            with suppressAndLogSendingException(msg):
                app.mail.send(msg)


def materialize_sell_in_reserve(sells: List[dict]):
    """Materializes the field 'sell' in reserve."""
    sell = sells[0]
    if 'reserve' in sell:
        DeviceEventDomain.update_one_raw(sell['reserve'], {'$set': {'sell': sell['_id']}})
