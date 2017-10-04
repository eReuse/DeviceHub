import base64
from typing import List, Set

from bson.objectid import ObjectId
from flask import current_app, g, request
from passlib.handlers.sha2_crypt import sha256_crypt
from passlib.utils import classproperty
from werkzeug.http import parse_authorization_header

from ereuse_devicehub.exceptions import BasicError, StandardError, UserHasExplicitDbPerms, WrongCredentials, \
    AuthHeaderError
from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.account.settings import AccountSettings
from ereuse_devicehub.resources.domain import Domain, ResourceNotFound
from ereuse_devicehub.security.perms import EXPLICIT_DB_PERMS, PARTIAL_ACCESS


class AccountDomain(Domain):
    resource_settings = AccountSettings

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
        """
        Gets the **unhashed** token. Use `hash_token` to hash it.
        :raise StandardError: The authorization header is invalid or missing.
        """
        try:
            # todo use g.user to get the token, something eve puts for us already
            x = request.headers.environ['HTTP_AUTHORIZATION']
            return parse_authorization_header(x)['username']
        except (KeyError, TypeError) as e:
            raise AuthHeaderError('The Authorization header is not well written or missing') from e

    @classproperty
    def requested_database(cls) -> str:
        """
        Gets the requested database in the URL. This is, the database name that is on the first path of the URL:
        www.foo.bar/db1.
        :raise NotADatabase: If the first path of the URL is not a database (ex. a neutral endpoint not tied to a db).
        """
        requested_database = request.path.split('/')[1]
        if requested_database not in current_app.config['DATABASES']:
            raise NotADatabase(requested_database)
        else:
            return requested_database

    @classproperty
    def auth_header(cls) -> str:
        """
        The actual authentication header.
        :raise StandardError: The authorization header is invalid or missing.
        """
        cls.actual_token  # Actual token will parse the header and ensure it is valid
        return request.headers.environ['HTTP_AUTHORIZATION']

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

    @classmethod
    def add_shared(cls, accounts_id: List[ObjectId] or Set[ObjectId], resource_type: str, db: str, _id: str or ObjectId,
                   label: str):
        """
        Materializes resource access to *shared* property of the account, and sets PARTIAL_ACCESS to
        the accounts. This method will raise an exception if there is an account with EXPLICIT_DB_PERMS.

        :raise UserHasExplicitDbPerms: You can't share to accounts that already have full access to this database.
        """
        q = {'_id': {'$in': accounts_id}, 'databases.' + db: {'$in': EXPLICIT_DB_PERMS}}
        accounts_explicit_access = cls.get(q)
        if len(list(accounts_explicit_access)) > 0:
            raise UserHasExplicitDbPerms(db, _id, resource_type, accounts_explicit_access)
        q = {
            '$push': {
                'shared': {
                    '_id': _id,
                    '@type': resource_type,
                    'db': db,
                    'label': label,
                    'baseUrl': current_app.config['BASE_URL_FOR_AGENTS']
                }
            },
            '$set': {
                'databases.{}'.format(db): PARTIAL_ACCESS
            }
        }
        cls.update_many_raw({'_id': {'$in': accounts_id}}, q)

    @classmethod
    def remove_shared(cls, db: str, accounts_id: Set[ObjectId], _id: str or ObjectId, type_name: str):
        """
        Removes devices from the *shared* field and removes PARTIAL_ACCESS from the database if there is
        no other shared resource in that database.
        """
        base_url = current_app.config['BASE_URL_FOR_AGENTS']
        for account_id in accounts_id:
            q = {'$pull': {'shared': {'_id': _id, '@type': type_name, 'db': db, 'baseUrl': base_url}}}
            cls.update_one_raw(account_id, q)
            try:
                cls.get_one({'shared': {'$elemMatch': {'db': db, 'baseUrl': base_url}}})
            except UserNotFound:
                cls.update_one_raw(account_id, {'$unset': {'shared.{}'.format(db): ''}})


class UserIsAnonymous(WrongCredentials):
    pass


class NoUserForGivenToken(WrongCredentials):
    pass


class NotADatabase(BasicError):
    status_code = 400

    def __init__(self, element: str):
        """
        :param element: The element that should have been a database.
        """
        self.element = element
        super().__init__({'element': element})


class CannotImportKey(StandardError):
    status_code = 400
    message = "We could not import the key. Make sure it is a valid GPG Public key."


class UserNotFound(ResourceNotFound):
    pass


class WrongHeader(StandardError):
    pass
