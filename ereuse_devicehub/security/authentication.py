from ereuse_devicehub.exceptions import UnauthorizedToUseDatabase
from ereuse_devicehub.resources.account.domain import AccountDomain, NotADatabase
from ereuse_devicehub.resources.account.role import Role
from eve.auth import TokenAuth
from flask import g, current_app


class RolesAuth(TokenAuth):
    def authorized(self, allowed_roles, resource, method):
        authorized = super(RolesAuth, self).authorized(allowed_roles, resource, method)
        if not authorized and method == 'GET':
            from ereuse_devicehub.resources.device.schema import Device
            if resource == 'devices' or resource in Device.resource_names:
                # We will check if the device is authorized in a hook, later
                # We avoid requesting the device at the database twice
                authorized = True
                self.set_needs_to_be_public()
                self._set_database(True)
            elif resource is None:  # schema (however will only load 'devices')
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
        if AccountDomain.actual:
            self._set_database()
            if allowed_roles and AccountDomain.actual['role'] >= allowed_roles[0]:
                if not AccountDomain.actual['role'].is_manager():
                    self.set_request_auth_value(AccountDomain.actual['_id'])
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
            requested_database = AccountDomain.get_requested_database()
        except NotADatabase as e:
            try:
                if e.body['requested_path'] not in current_app.config['RESOURCES_NOT_USING_DATABASES'] \
                        and not current_app.config['DOMAIN'][e.body['requested_path']]['use_default_database']:
                    raise e
            except KeyError:
                raise e
        else:
            if force or (requested_database in AccountDomain.actual['databases']
                         or AccountDomain.actual['role'] == Role.SUPERUSER):
                self.set_mongo_prefix(requested_database.replace("-", "").upper())
            else:
                raise UnauthorizedToUseDatabase()

    @staticmethod
    def set_needs_to_be_public(value: bool = True):
        g.needs_to_be_public = value

    @staticmethod
    def needs_to_be_public() -> bool:
        return getattr(g, 'needs_to_be_public', False)
