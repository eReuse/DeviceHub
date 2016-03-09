from eve.auth import TokenAuth
from flask import g, current_app

from app.account.user import User, Role, NotADatabase
from app.exceptions import UnauthorizedToUseDatabase


class RolesAuth(TokenAuth):
    def authorized(self, allowed_roles, resource, method):
        authorized = super(RolesAuth, self).authorized(allowed_roles, resource, method)
        if not authorized and method == 'GET' and resource == 'devices':
            # We will check if the device is authorized in a hook, later
            # We avoid requesting the device at the database twice
            self.set_needs_to_be_public()
            self._set_database(True)
            authorized = True
        return authorized

    def check_auth(self, token, allowed_roles, resource, method):
        """
        :param token:
        :param allowed_roles: List of JUST ONE Role
        :param resource:
        :param method:
        """

        # use Eve's own db driver; no additional connections/resources are used
        has_perm = False
        if User.actual:
            self._set_database()
            if allowed_roles and User.actual['role'] >= allowed_roles[0]:
                if not User.actual['role'].is_manager():
                    self.set_request_auth_value(User.actual['_id'])
                has_perm = True
            elif not allowed_roles:
                has_perm = True
        return has_perm

    def _set_database(self, force: bool = False):
        """
        Sets the actual database according of the value in the URL.
        :param force: Sets the database even if the user has no access to it
        :raises NotADatabase: When the URL is malformed or doesn't contain an existing database
        :raises UnauthorizedToUseDatabase: If force is true this won't raise
        """
        try:
            requested_database = User.get_requested_database()
        except NotADatabase as e:
            if e.body['requested_path'] not in current_app.config['RESOURCES_NOT_USING_CUSTOM_DATABASES']:
                raise e
        else:
            if force or (requested_database in User.actual['databases'] or User.actual['role'] == Role.SUPERUSER):
                g.auth_requested_database = requested_database
                self.set_mongo_prefix(requested_database.replace("-", "").upper())
            else:
                raise UnauthorizedToUseDatabase()

    @staticmethod
    def get_requested_database_for_uri() -> str:
        try:
            return g.auth_requested_database + '/'
        except KeyError:
            return ''

    @staticmethod
    def set_needs_to_be_public(value: bool = True):
        g.needs_to_be_public = value

    @staticmethod
    def needs_to_be_public() -> bool:
        return getattr(g, 'needs_to_be_public', False)
