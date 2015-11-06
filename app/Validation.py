from app.accounts.User import User

__author__ = 'busta'

from eve.io.mongo import Validator

ALLOWED_WRITE_ROLES = 'dh_allowed_write_roles'
DEFAULT_AUTHOR = 'dh_default_author'

class DeviceHubValidator(Validator):
    def _validate_dh_allowed_write_roles(self, roles, field, value):
        if not User.actual['role'] in roles:
            self._error(field, "You do not have permission to write field " + field + ".")
