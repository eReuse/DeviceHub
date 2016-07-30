import base64

from bson.objectid import ObjectId
from flask import current_app
from flask import g
from flask import request
from werkzeug.http import parse_authorization_header

from ereuse_devicehub.exceptions import WrongCredentials, BasicError, StandardError
from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.account.settings import AccountSettings
from ereuse_devicehub.resources.domain import Domain, ResourceNotFound
from ereuse_devicehub.utils import ClassProperty


class AccountDomain(Domain):
    resource_settings = AccountSettings
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
                    g._actual_user = AccountDomain.get_one({'token': token})
                    g._actual_user['role'] = Role(g._actual_user['role'])
                except UserNotFound:
                    raise UserIsAnonymous("You need to be logged in.")
                except TypeError:
                    raise NoUserForGivenToken()
            return g._actual_user
        except RuntimeError as e:
            # Documentation access this variable
            if str(e) != 'working outside of application context':
                raise e

    @classmethod
    def get_one(cls, id_or_filter: dict or ObjectId or str):
        try:
            return super().get_one(id_or_filter)
        except ResourceNotFound:
            raise UserNotFound()

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


class UserIsAnonymous(WrongCredentials):
    pass


class NoUserForGivenToken(WrongCredentials):
    pass


class NotADatabase(BasicError):
    status_code = 400


class CannotImportKey(StandardError):
    status_code = 400
    message = "We could not import the key. Make sure it is a valid GPG Public key."


class UserNotFound(ResourceNotFound):
    pass