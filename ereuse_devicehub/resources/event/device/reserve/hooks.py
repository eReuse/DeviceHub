from typing import List

from flask import current_app as app, g
from pydash import pluck

from ereuse_devicehub.mails.mails import create_email, suppressAndLogSendingException
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.event.device.reserve.settings import Reserve
from ereuse_devicehub.security.auth import Auth
from ereuse_devicehub.security.perms import EXPLICIT_DB_PERMS
from ereuse_devicehub.utils import url_for_resource


def set_for_and_notify(reserves: List[dict]):
    """Sets the fields 'for' and 'notify' of the reserves."""
    for reserve in reserves:
        # 'for'
        if 'for' not in reserve or not Auth.has_full_db_access():
            reserve['for'] = AccountDomain.actual['_id']
        # 'notify'
        db = AccountDomain.requested_database
        # We notify to accounts that own the database and represent real users (not machines)
        q = {
            'databases.{}'.format(db): {'$in': EXPLICIT_DB_PERMS},
            'role': {'$nin': Role.MACHINES},
            'active': True
        }
        accounts_with_full_access = AccountDomain.get(q)
        reserve['notify'] = pluck(accounts_with_full_access, '_id')
        g.dh_device_event_reserve_notify = accounts_with_full_access


def notify(reserves: List[dict]):
    """Sends e-mails to the 'notify' and 'for' accounts of the reserves."""
    msgs = []
    context = {
        'fields': (
            {'path': '_id', 'name': 'ID in ' + AccountDomain.requested_database},
            {'path': '@type', 'name': 'Type'},
            {'path': 'type', 'name': 'Subtype'},
            {'path': 'serialNumber', 'name': 'S/N'}
        )
    }
    for reserve in reserves:
        context['devices'] = DeviceDomain.get_in('_id', reserve['devices'])
        context['reserve_url'] = url_for_resource(Reserve.resource_name, reserve['_id'])
        _for = AccountDomain.get_one(reserve['for'])
        if _for['active']:
            msgs.append(create_email('mails/reserve_for.html', _for, **context))
        context['for'] = _for
        for recipient in g.get('dh_device_event_reserve_notify', []):
            msgs.append(create_email('mails/reserve_notify.html', recipient, **context))
    # We send all emails with the same connection (+ speed)
    with app.mail.connect() as conn:
        for msg in msgs:
            with suppressAndLogSendingException(msg):
                conn.send(msg)
