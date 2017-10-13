from ereuse_devicehub import DeviceHub
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.event.domain import EventDomain
from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.group.settings import Group
from ereuse_devicehub.scripts.updates.update import Update


class DatabaseUpdate07:
    """sets new default fields to the database."""
    def __init__(self, app) -> None:
        DatabaseUpdate07A(app)
        DatabaseUpdate07B(app)


class DatabaseUpdate07A:
    def __init__(self, app: DeviceHub, **kwargs) -> None:
        app.config['DEBUG'] = True  # Print log messages on screen
        with app.app_context():
            count = 0
            for account in AccountDomain.get({}):
                if 'active' not in account:
                    print('Add active field to account {}'.format(account.get('email', account['_id'])))
                    AccountDomain.update_one_raw(account['_id'], {'$set': {'active': True}})
                    count += 1
                if 'shared' not in account:
                    AccountDomain.update_one_raw(account['_id'], {'$set': {'shared': []}})
            print('We added active to {} accounts'.format(count))


class DatabaseUpdate07B(Update):
    def execute(self, database):
        for event in EventDomain.get({}):
            if 'perms' not in event:
                EventDomain.update_one_raw(event['_id'], {'$set': {'perms': []}})

        for resource_name, childDomain in GroupDomain.children_resources.items():
            for resource in childDomain.get({}):
                if 'perms' not in resource:
                    childDomain.update_one_raw(resource['_id'], {'$set': {'perms': []}})
                if resource_name in Group.resource_names and 'sharedWith' not in resource:
                    childDomain.update_one_raw(resource['_id'], {'$set': {'sharedWith': []}})
