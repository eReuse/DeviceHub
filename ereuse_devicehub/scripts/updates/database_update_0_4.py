from flask import current_app

from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.exceptions import DeviceNotFound
from ereuse_devicehub.resources.event.domain import EventDomain
from ereuse_devicehub.resources.group.physical.place.domain import PlaceDomain
from ereuse_devicehub.rest import execute_patch
from ereuse_devicehub.scripts.updates.update import Update


class DatabaseUpdate04(Update):
    """
        Updates the database to the version 0.4 of DeviceHub.

        Version 0.4 adds groups. This updates the fk of places in devices and the fk of devices in places.

        Note that this method
    """

    def execute(self, database):
        #ids
        all_places = PlaceDomain.get({})
        PlaceDomain.delete_all()
        for place in all_places:
            old_place_id = place['_id']
            place['_id'] = str(current_app.sid.generate())
            PlaceDomain.insert(place)
            # events
            EventDomain.update_many_raw({'place': old_place_id}, {'$set': {'place': place['_id']}})
        # devices
        if database == 'alencop':
            DeviceDomain.update_many_raw({}, {'$unset': {'place': ''}})
            PlaceDomain.delete_all()
        else:
            PlaceDomain.update_many_raw({}, {'$set': {'children': {}, 'ancestors': []}})  # set as default
            for place in PlaceDomain.get({'devices': {'$exists': True}}):
                if place.get('devices', None):
                    patch = {'children': {'devices': place['devices']}, '@type': 'Place'}
                    for device_id in list(place['devices']):
                        try:
                            DeviceDomain.get_one(device_id)
                        except DeviceNotFound:
                            place['devices'].remove(device_id)
                    account = AccountDomain.get_one(place['byUser'])
                    headers = (('Accept', 'application/json'),
                               ('Authorization', 'Basic ' + AccountDomain.hash_token(account['token']).decode()))
                    with self.app.test_request_context('/{}/devices'.format(database), headers=headers):
                        execute_patch('places', patch, identifier=place['_id'], copy_id=False)
                    # PlaceDomain.update_many_raw(QUERY, {'$unset': {'devices': True}})
        # events

