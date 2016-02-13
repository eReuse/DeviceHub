from eve.auth import TokenAuth

from app.account.user import User, Role, NotADatabase
from flask import g, current_app
from app.exceptions import UnauthorizedToUseDatabase


class RolesAuth(TokenAuth):
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

    def _set_database(self):
        try:
            requested_database = User.get_requested_database()
        except NotADatabase as e:
            if e.body['requested_path'] not in current_app.config['RESOURCES_NOT_USING_CUSTOM_DATABASES']:
                raise e
        else:
            if requested_database in User.actual['databases'] or User.actual['role'] == Role.SUPERUSER:
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
