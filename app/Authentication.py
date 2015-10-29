from eve.auth import TokenAuth

from app.accounts.User import User
from app.config import MANAGERS

__author__ = 'busta'

class RolesAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        """For the purpose of this example the implementation is as simple as
        possible. A 'real' token should probably contain a hash of the
        username/password combo, which sould then validated against the account
        data stored on the DB.
        """
        # use Eve's own db driver; no additional connections/resources are used
        has_perm = False
        if User.actual:
            if allowed_roles and User.actual['role'] in allowed_roles:
                if User.actual['role'] not in MANAGERS:
                    self.set_request_auth_value(User.actual['_id'])
                    has_perm = True
            elif not allowed_roles:
                has_perm = True
        return has_perm
"""
    def check_post(self, resource, account):
        from settings import DOMAIN
        from flask import request
        for field_name, field in DOMAIN[resource]['schema'].items():
            if ALLOWED_WRITE_ROLES in field and field_name in request.json:
                return account['role'] in ALLOWED_WRITE_ROLES
        return True
"""

class AccountAuth(RolesAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        return super(AccountAuth, self).check_auth(token, allowed_roles, resource, method)


