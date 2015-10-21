from eve.auth import TokenAuth, BasicAuth

__author__ = 'busta'

class RolesAuth(TokenAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        """For the purpose of this example the implementation is as simple as
        possible. A 'real' token should probably contain a hash of the
        username/password combo, which sould then validated against the account
        data stored on the DB.
        """
        from app.app import app
        # use Eve's own db driver; no additional connections/resources are used
        accounts = app.data.driver.db['accounts']
        lookup = {'token': token}
        if allowed_roles:  # only retrieve a user if his roles match ``allowed_roles``
            lookup['roles'] = {'$in': allowed_roles}
        account = accounts.find_one(dict(lookup))
        if account and app.config['ADMIN'] not in account['roles']:
            # if the user is not an admin, we need to check for some things:
            if account and '_id' in account:
                # for the domains (and only those) that have 'auth_field' in their settings, activate the checking.
                self.set_request_auth_value(account['_id'])
        return account


class AccountAuth(RolesAuth):
    def check_auth(self, token, allowed_roles, resource, method):
        super()