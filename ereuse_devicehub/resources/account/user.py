import base64

from bson.objectid import ObjectId
from flask import current_app
from flask import g
from flask import request
from werkzeug.http import parse_authorization_header

from ereuse_devicehub.exceptions import WrongCredentials, BasicError, StandardError
from ereuse_devicehub.utils import ClassProperty


class User:
    @staticmethod
    def get_requested_database():
        requested_database = request.path.split('/')[1]
        if requested_database not in current_app.config['DATABASES']:
            raise NotADatabase({'requested_path': requested_database})
        else:
            return requested_database

    # noinspection PyNestedDecorators
    @ClassProperty
    @classmethod
    def actual(cls) -> dict:
        try:
            if not hasattr(g, '_actual_user'):
                from flask import request
                try:
                    x = request.headers.environ['HTTP_AUTHORIZATION']
                    token = parse_authorization_header(x)['username']
                    from flask import current_app as app
                    g._actual_user = User.get({'token': token})
                    g._actual_user['role'] = Role(g._actual_user['role'])
                except KeyError:
                    raise UserIsAnonymous("You need to be logged in.")
                except TypeError:
                    raise NoUserForGivenToken()
            return g._actual_user
        except RuntimeError as e:
            # Documentation access this variable
            if str(e) != 'working outside of application context':
                raise e

    @staticmethod
    def get(account_id_or_query: ObjectId or dict):
        return current_app.data.find_one_raw('accounts', account_id_or_query)

    @staticmethod
    def import_key(key: str) -> str:
        """
        Imports the key for the user
        :param key: GPG Public Key
        :raises CannotImportKey:
        :return: Fingerprint of the imported key
        """
        result = current_app.gpg.import_keys(key)
        if result.count == 0:
            raise CannotImportKey()
        return result.fingerprint[0]

    @staticmethod
    def hash_token(token):
        return base64.b64encode(
            str.encode(token + ':'))  # Framework needs ':' at the end before send it to client


class Role:
    """
    Roles specify what users can do generally.
    Locations alter what users can do. Locations permissions > roles. Admins don't get affected by location perms.
    Roles are ordered hierarchically. This means that an amateur role has the same permissions as a basic, and more.
    An employee can do the same as an amateur, and more.
    The gradient is:
    BASIC < AMATEUR < EMPLOYEE < ADMIN < SUPERUSER

    We can use operators to compare between roles. For example BASIC < AMATEUR == True
    """
    BASIC = 'basic'
    """Most basic user. Cannot do anything (except its account). Useful for external people."""
    AMATEUR = 'amateur'
    """Can create devices, however can just see and edit the ones it created. Events are restricted."""
    EMPLOYEE = 'employee'
    """Technicians. Full spectre of operations. Can interact with devices of others."""
    ADMIN = 'admin'
    """worker role + manage other users (except superusers). No location restrictions. Can see analytics."""
    SUPERUSER = 'superuser'
    """admin + they don't appear as public users, and they can manage other superusers. See all databases."""
    ROLES = BASIC, AMATEUR, EMPLOYEE, ADMIN, SUPERUSER
    """In grading order (BASIC < AMATEUR)"""
    MANAGERS = ADMIN, SUPERUSER

    def __init__(self, representation):
        if representation not in self.ROLES:
            raise TypeError(representation + ' is not a role.')
        self.role = representation

    def is_manager(self):
        return self.role in self.MANAGERS

    def has_role(self, roles: set):
        return self.role in roles

    def __lt__(self, other):
        if isinstance(other, Role):
            return self.ROLES.index(self.role) < self.ROLES.index(other.role)
        elif isinstance(other, str):
            return self.ROLES.index(self.role) < self.ROLES.index(other)
        else:
            raise NotImplemented

    def __le__(self, other):
        if isinstance(other, Role):
            return self.ROLES.index(self.role) <= self.ROLES.index(other.role)
        elif isinstance(other, str):
            return self.ROLES.index(self.role) <= self.ROLES.index(other)
        else:
            raise NotImplemented

    def __gt__(self, other):
        return not self.__le__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        if isinstance(other, Role):
            return self.role == other.role
        elif isinstance(other, str):
            return self.role == other
        else:
            raise NotImplemented

    def __hash__(self):
        return self.role.__hash__()


class UserIsAnonymous(WrongCredentials):
    pass


class NoUserForGivenToken(WrongCredentials):
    pass


class NotADatabase(BasicError):
    status_code = 400


class CannotImportKey(StandardError):
    status_code = 400
    message = "We could not import the key. Make sure it is a valid GPG Public key."
