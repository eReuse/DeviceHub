import json
import sys
from pprint import pprint

from pymongo import MongoClient

from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.resources.account.hooks import hash_password, generate_token
from ereuse_devicehub.resources.account.domain import AccountDomain


def create_account(email: str, password: str, databases: list,
                   role: str = None, name: str = None, organization: str = None, blocked: bool = False,
                   default_database: str = None, mongo_host: str = None, mongo_port: int = None,
                   db_name: str = 'dh__accounts'):
    """
    Creates an account. You can call the file directly::

        create_account.py b@b.b 123 [\'db1\'] superuser

    :param email:
    :param password:
    :param databases: The databases the user has access to
    :param mongo_host: Leave empty to use default.
    :param mongo_port: Leave empty to use default.
    :param db_name: The name of the database to create the account to. Leave empty to use default.
    :param default_database: if none we use the first database of *databases*.
    :param role: the role of the user, if none, we use the default set in Account type.
    :param name:
    :param organization:
    :param blocked: False if it is not set
    :throws UserAlreadyExists:
    :return: The account with the *base256* token and *hashed* password.
    """
    connection = MongoClient(mongo_host, mongo_port)
    db = connection[db_name]
    if db.accounts.find_one({'email': email}):
        raise UserAlreadyExists()
    databases = eval(databases)
    if type(databases) is not list:
        raise TypeError('databases has to be a list')
    account = {
        'email': email,
        'password': password,
        'databases': databases,
        'defaultDatabase': default_database or databases[0],
        '@type': 'Account',
        'blocked': eval(blocked) if type(blocked) is str else blocked,
        'active': True
    }
    if role is not None:
        account['role'] = role
    if name is not None:
        account['name'] = name
    if organization is not None:
        account['organization'] = organization
    token = generate_token()
    while db.accounts.find_one({'token': token}) is not None:
        token = generate_token()
    account["token"] = token
    hash_password([account])
    db.accounts.insert(account)
    returned_account = db.accounts.find_one({'email': email})
    return returned_account, AccountDomain.hash_token(returned_account['token'])


class UserAlreadyExists(StandardError):
    message = 'User already exists'
    code = 309


if __name__ == '__main__':
    # comment this for autodoc to work. todo Why does it fail?
    account, hashed_token = create_account(*sys.argv[1:])
    account['_id'] = str(account['_id'])
    print('Account:')
    print(json.dumps(account, indent=4))
    print('Hashed token for REST:')
    print(hashed_token)
