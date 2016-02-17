import random
import string

from passlib.handlers.sha2_crypt import sha256_crypt

from app.account.user import User, Role
from app.app import app
from app.rest import execute_post

def hash_password(accounts: list):
    for account in accounts:
        if account['active']:
            account['password'] = sha256_crypt.encrypt(account['password'])

def add_token(documents: list):
    for document in documents:
        token = generate_token()
        while app.data.driver.db['accounts'].find_one({'token': token}) is not None:
            token = generate_token()
        document["token"] = token


def generate_token() -> str:
    return (''.join(random.choice(string.ascii_uppercase)
                    for x in range(10)))


def set_byUser(resource_name: str, items: list):
    from app.app import app
    if 'byUser' in app.config['DOMAIN'][resource_name]['schema']:
        for item in items:
            item['byUser'] = User.actual['_id']


def set_default_database_if_empty(accounts: list):
    for account in accounts:
        if 'defaultDatabase' not in account and account['role'] != Role.SUPERUSER:
            account['defaultDatabase'] = account['databases'][0]


def add_or_get_inactive_account(events: list):
    # todo if register we need to make sure that user does not add the account again another time (usability?)
    for event in events:
        if event['@type'] == 'Receive':
            _add_or_get_inactive_account_id(event, 'unregisteredReceiver', 'receiver')
        elif event['@type'] == 'Allocate':
            _add_or_get_inactive_account_id(event, 'unregisteredTo', 'to')


def _add_or_get_inactive_account_id(event, field_name, recipient_field_name):
    if field_name in event:
        try:
            _id = app.data.driver.db.accounts.find_one(
                {
                    'email': event[field_name]['email'],
                    'databases': {'$in': User.actual['databases']}  # We look for just accounts that share our database
                }
            )['_id']
        except TypeError:  # No account
            event[field_name]['databases'] = User.actual['databases']
            event[field_name]['active'] = False
            _id = execute_post('accounts', event[field_name])['_id']
        event[recipient_field_name] = _id
        del event[field_name]
