from ereuse_devicehub import DeviceHub
from ereuse_devicehub.resources.account.domain import AccountDomain


class DatabaseUpdate07:
    def __init__(self, app: DeviceHub, **kwargs) -> None:
        app.config['DEBUG'] = True  # Print log messages on screen
        with app.app_context():
            count = 0
            for account in AccountDomain.get({}):
                if 'active' not in account:
                    print('Add active field to account {}'.format(account.get('email', account['_id'])))
                    AccountDomain.update_one_raw(account['_id'], {'$set': {'active': True}})
                    count += 1
            print('We added active to {} accounts'.format(count))
