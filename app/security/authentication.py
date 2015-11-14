from eve.auth import TokenAuth

from app.accounts.user import User


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
                if not User.actual['role'].is_manager():
                    self.set_request_auth_value(User.actual['_id'])
                has_perm = True
            elif not allowed_roles:
                has_perm = True
        return has_perm
