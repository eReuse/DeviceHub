from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.scripts.updates.update import Update
from ereuse_devicehub.security.perms import ADMIN


class DatabaseUpdate06(Update):
    """
        Updates the database to the version 0.6 of DeviceHub.

        Version 0.6 adds permissions.
    """
    ROLE_DICT = {
        'basic': Role.USER,
        'amateur': Role.USER,
        'employee': Role.USER,
        'admin': Role.USER,  # old admins do not map to new admins
        'superuser': Role.SUPERUSER
    }

    def execute(self, database):
        DeviceDomain.update_many_raw({}, {'$set': {'perms': []}})
        GroupDomain.update_many_raw({}, {'$set': {'perms': [], 'sharedWith': []}})
        for account in AccountDomain.get({}):
            dbs = {db: ADMIN for db in account['databases']}
            role = self.ROLE_DICT[account['role']]
            q = {'$set': {'databases': dbs, 'role': role, 'shared': []}}
            AccountDomain.update_one_raw(account['_id'], q)
