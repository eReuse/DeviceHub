from typing import List

from flask import current_app as app

from ereuse_devicehub.mails.mails import create_email
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.event.device.reserve.settings import Reserve
from ereuse_devicehub.utils import url_for_resource


def notify(sells: List[dict]):
    for sell in sells:
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
        to = AccountDomain.get_one(sell['to'])
        msg = create_email('mails/sell.html', to, **context)
        app.mail.send(msg)
