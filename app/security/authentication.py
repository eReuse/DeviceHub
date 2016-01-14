from eve.auth import TokenAuth

from app.account.user import User
from flask import request
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
        requested_database = request.path.split('/')[1]
        if requested_database in User.actual['databases']:
            self.set_mongo_prefix(requested_database.replace("-", "").upper())
        else:
            raise UnauthorizedToUseDatabase()