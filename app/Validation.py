from eve.io.mongo import Validator

from app.accounts.User import User

ALLOWED_WRITE_ROLES = 'dh_allowed_write_roles'
DEFAULT_AUTHOR = 'dh_default_author'
OR = 'dh_or'


class DeviceHubValidator(Validator):
    def _validate_dh_allowed_write_roles(self, roles, field, value):
        if not User.actual['role'] in roles:
            self._error(field, "You do not have permission to write field " + field + ".")

    def _validate_dh_or(self, list_of_names, field, value):
        for name in list_of_names:
            if name in self.document:
                return
        self._error(list_of_names[0], "You need to set one of these: " + str(list_of_names))
