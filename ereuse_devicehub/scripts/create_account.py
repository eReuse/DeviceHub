import argparse
import json
from getpass import getpass

from pymongo import MongoClient

from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.account.hooks import hash_password, generate_token
from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.security.perms import ADMIN


def create_account(email: str, password: str, databases: list,
                   role: str = Role.USER, name: str = None, organization: str = None, blocked: bool = False,
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
    account = {
        'email': email,
        'password': password,
        'databases': {db: ADMIN for db in databases},
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
    db.accounts.insert_one(account)
    returned_account = db.accounts.find_one({'email': email})
    return returned_account, AccountDomain.hash_token(returned_account['token'])


class UserAlreadyExists(StandardError):
    message = 'User already exists'
    code = 309


if __name__ == '__main__':
    # comment this for autodoc to work. todo Why does it fail?
    desc = 'Create an account. This script connects directly to a Mongo interface, so you need to set the connection.'
    epilog = 'Minimum example: python create_account.py a@a.a -d db1 db2'
    parser = argparse.ArgumentParser(description=desc, epilog=epilog)
    parser.add_argument('email')
    parser.add_argument('-d', '--databases', nargs='+', required=True,
                        help='Required. A list of databases the user has access to.')
    parser.add_argument('-r', '--role', help='By default is admin.', default=Role.USER)
    parser.add_argument('-n', '--name')
    parser.add_argument('-o', '--organization')
    parser.add_argument('-b', '--blocked', action='store_true')
    parser.add_argument('-f', '--default-database',
                        help='The default database. Leave it empty to use the first of the databases parameter.')
    parser.add_argument('-mh', '--mongo-host', help='Leave it empty to connect to the default Mongo interface URL.')
    parser.add_argument('-mp', '--mongo-port', help='Leave it empty to connect to the default Mongo interface port.')
    parser.add_argument('-dn', '--db-name', default='dh__accounts',
                        help='The database in Mongo used to store the account.')
    args = vars(parser.parse_args())  # If --help or -h or wrong value this will print message to user and abort
    args['password'] = getpass('Enter new password for {}: '.format(args['email']))
    account, hashed_token = create_account(**args)
    account['_id'] = str(account['_id'])
    print('Account:')
    print(json.dumps(account, indent=4))
    print('Hashed token for REST:')
    print(hashed_token)
