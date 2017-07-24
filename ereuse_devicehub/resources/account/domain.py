import base64

from bson.objectid import ObjectId
from flask import current_app
from flask import g
from flask import request
from passlib.handlers.sha2_crypt import sha256_crypt
from passlib.utils import classproperty
from werkzeug.http import parse_authorization_header

from ereuse_devicehub.exceptions import WrongCredentials, BasicError, StandardError
from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.account.settings import AccountSettings
from ereuse_devicehub.resources.domain import Domain, ResourceNotFound


class AccountDomain(Domain):
    resource_settings = AccountSettings

    @staticmethod
    def get_requested_database():
        requested_database = request.path.split('/')[1]
        if requested_database not in current_app.config['DATABASES']:
            raise NotADatabase({'requested_path': requested_database})
        else:
            return requested_database

    @classproperty
    def actual(cls) -> dict:
        try:
            # the values of g are inherited when doing inner requests so we need
            # to always check the token in the headers (cls.actual_token)
            # https://stackoverflow.com/questions/20036520/what-is-the-purpose-of-flasks-context-stacks
            # http://stackoverflow.com/a/33382823/2710757
            token = cls.actual_token
            if not hasattr(g, '_actual_user') or g._actual_user['token'] != token:
                from flask import request
                try:
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

    @classproperty
    def actual_token(cls) -> str:
        """Gets the **unhashed** token. Use `hash_token` to hash it."""
        try:
            x = request.headers.environ['HTTP_AUTHORIZATION']
            return parse_authorization_header(x)['username']
        except (KeyError, TypeError) as e:
            raise StandardError('The Authorization header is not well written or missing', 400) from e

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
        # Framework needs ':' at the end before send it to client
        return base64.b64encode(str.encode(token + ':'))

    @staticmethod
    def encrypt_password(password: str) -> str:
        return sha256_crypt.hash(password)

    @staticmethod
    def verify_password(password: str, original: str) -> bool:
        return sha256_crypt.verify(password, original)


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


class WrongHeader(StandardError):
    pass
