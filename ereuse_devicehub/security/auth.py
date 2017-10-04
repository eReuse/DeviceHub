from contextlib import contextmanager, suppress

from ereuse_devicehub.resources.account.role import Role
from eve.auth import TokenAuth
from flask import current_app as app
from werkzeug.exceptions import NotFound

from ereuse_devicehub.resources.account.domain import AccountDomain, NotADatabase
from ereuse_devicehub.security.perms import DB_PERMS, EXPLICIT_DB_PERMS


class Auth(TokenAuth):
    """
    Authorization module for DeviceHub. Handles Authorization and sets the database from the segment of the URL.
    """
    METHODS = {'GET', 'POST'}

    def check_auth(self, token: str, _, resource: str, method: str) -> bool:
        """
        Checks if user has access to this resource. Access is granted if:
        - User is logged in (there is a valid token in the headers)
        - One of both:
          - User is accessing a resource that uses the default database (like accounts or schema)
          - User is accessing a resource that uses an inventory or specific database (like devices) and user has access
            to such database. In this case, the hook *check_perms* from this module will check later that the user
            has access to the specific resources (ex: device #29), as this method cannot access to the data to verify
            this.
        """
        _ = AccountDomain.actual
        requested_db = self.set_database_from_url()

        return (self.has_full_db_access() or method in self.METHODS and self.db_access()) if requested_db else True

    def set_database_from_url(self) -> str or None:
        """
        Set the actual database according of the value in the URL.
        :param force: Sets the database even if the user has no access to it.
        :raise NotADatabase: When the URL is malformed or doesn't contain an existing database.
        :return The name of database or None.
        """
        requested_db = None
        try:
            requested_db = AccountDomain.requested_database
        except NotADatabase as e:
            # databases are set in the first path of the url: www.foo.com/db1/...
            # except for endpoints like schema or resources like account.
            # In those cases we won't set the database, as eve already
            # set the default database
            endpoint = e.element
            # Note that this method raises a 404 if the endpoint does not exist in devicehub
            if not self.uses_default_db(endpoint):
                raise e
        else:
            self.set_mongo_prefix(requested_db.replace('-', '').upper())
        return requested_db

    @staticmethod
    def uses_default_db(endpoint: str) -> bool:
        """
        Does the endpoint (like 'schema') or resource endpoint (like 'devices') use a default database?

        - schema uses a default db
        - account uses a default db
        - devices doesn't use a default db
        - ...

        :raise NotFound: The resource or endpoint is not defined in this DHub. This is standard 404 not found.
        """
        try:
            return endpoint in app.config['RESOURCES_NOT_USING_DATABASES'] or \
                   app.config['DOMAIN'][endpoint].get('use_default_database', False)
        except KeyError:
            raise NotFound()

    @staticmethod
    def has_db_perm(account: dict, db: str, perm: str) -> bool:
        """Has the account a specific type of access to a database?"""
        if perm not in DB_PERMS:
            raise TypeError('{} must be a valid permission'.format(perm))
        return perm == account['databases'].get(db, None)

    @staticmethod
    def db_access(account: dict = None, db: str = None) -> str or None:
        """
        Returns the db access of the account, or None. You can safely do *if db_access(...):*
        :param account: If none, the actual account is used.
        :param db: If none, the actual db is used.
        """
        account = account or AccountDomain.actual
        db = db or AccountDomain.requested_database
        return account['databases'].get(db, None)

    @staticmethod
    def has_full_db_access(account: dict = None, db: str = None) -> bool:
        """
        Has the account full access to the database?
        :param account: If none, the actual account is used.
        :param db: If none, the actual db is used.
        """
        account = account or AccountDomain.actual
        db = db or AccountDomain.requested_database
        return account['role'] == Role.SUPERUSER or account['databases'].get(db, None) in EXPLICIT_DB_PERMS

    @contextmanager
    def database(self, database: str, headers=None):
        """Set the actual database, reverting after to the old database, if need it. To use with 'with'."""
        # We need to have an active request to 'trick' set_database and work with the database we want
        from flask import current_app as app
        with suppress(NotADatabase):
            # Let's get the old
            mongo_prefix = self.get_mongo_prefix()
        with app.test_request_context('/{}/devices'.format(database), headers=headers):
            self.set_database_from_url()
            yield
        if mongo_prefix:
            self.set_mongo_prefix(mongo_prefix)
