from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.group.physical.place.domain import PlaceDomain
from ereuse_devicehub.rest import execute_patch
from ereuse_devicehub.scripts.updates.update import Update


class DatabaseUpdate03(Update):
    """
        Updates the database to the version 0.3 of DeviceHub.

        Version 0.3 adds groups. This updates the fk of places in devices and the fk of devices in places.

        Note that this method
    """

    def execute(self, database):
        QUERY = {'devices': {'$exists': True}}
        # devices
        PlaceDomain.update_many_raw({}, {'$set': {'children': {}, 'ancestors': []}})  # set as default
        for place in PlaceDomain.get(QUERY):
            patch = {'children': {'devices': place['devices']}, '@type': 'Place'}
            account = AccountDomain.get_one({'email': 'a@a.a'})
            headers = (('Accept', 'application/json'),
                       ('Authorization', 'Basic ' + AccountDomain.hash_token(account['token']).decode()))
            with self.app.test_request_context('/{}/devices'.format(database), headers=headers):
                execute_patch('places', patch, identifier=place['_id'])
            # PlaceDomain.update_many_raw(QUERY, {'$unset': {'devices': True}})
