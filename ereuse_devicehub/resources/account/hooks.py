import random
import string

from ereuse_devicehub.resources.account.domain import AccountDomain, UserNotFound
from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.rest import execute_post
from flask import current_app as app
from passlib.handlers.sha2_crypt import sha256_crypt


def hash_password(accounts: list):
    for account in accounts:
        if 'password' in account:
            account['password'] = sha256_crypt.encrypt(account['password'])


def add_token(documents: list):
    for document in documents:
        token = generate_token()
        while app.data.find_one_raw('accounts', {'token': token}) is not None:
            token = generate_token()
        document["token"] = token


def generate_token() -> str:
    return (''.join(random.choice(string.ascii_uppercase)
                    for x in range(10)))


# noinspection PyPep8Naming
def set_byUser(resource_name: str, items: list):
    if 'byUser' in app.config['DOMAIN'][resource_name]['schema']:
        for item in items:
            if 'byUser' not in item:
                item['byUser'] = AccountDomain.actual['_id']


# noinspection PyPep8Naming
def set_byOrganization(resource_name: str, items: list):
    """
    Sets the 'byOrganization' field, which is the materialization of the organization of byUser (the actual user).
    This materialization shall no be updated when the user's organization changes.
    """
    for item in items:
        if 'byOrganization' in app.config['DOMAIN'][resource_name]['schema']:
            if 'organization' in AccountDomain.actual:
                item['byOrganization'] = AccountDomain.actual['organization']


def set_default_database_if_empty(accounts: list):
    for account in accounts:
        if 'defaultDatabase' not in account and account['role'] != Role.SUPERUSER:
            account['defaultDatabase'] = account['databases'][0]


def add_or_get_inactive_account_receive(events: list):
    for event in events:
        _add_or_get_inactive_account_id(event, 'receiver')


def add_or_get_inactive_account_allocate(events: list):
    for event in events:
        _add_or_get_inactive_account_id(event, 'to')


def add_or_get_inactive_account_snapshot(events: list):
    for event in events:
        _add_or_get_inactive_account_id(event, 'from')


def _add_or_get_inactive_account_id(event, field_name):
    """
    We need to execute after insert and insert_resource.
    """
    if field_name in event and type(event[field_name]) is dict:
        try:
            # We look for just accounts that share our database
            _id = AccountDomain.get_one({
                'email': event[field_name]['email'] # 'databases': {'$in': AccountDomain.actual['databases']} todo review this
            })['_id']
        except UserNotFound:
            event[field_name]['databases'] = [AccountDomain.get_requested_database()]
            event[field_name]['active'] = False
            event[field_name]['@type'] = 'Account'
            _id = execute_post('accounts', event[field_name], True)['_id']
        event[field_name] = _id
