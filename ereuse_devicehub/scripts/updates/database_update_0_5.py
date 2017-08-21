from contextlib import suppress

import pymongo

from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.event.device.domain import DeviceEventDomain
from ereuse_devicehub.scripts.updates.update import Update


class DatabaseUpdate05(Update):
    """
        Updates the database to the version 0.5 of DeviceHub.

        Version 0.5 materializes snapshot's condition field into devices.
    """

    def execute(self, database):
        for device in DeviceDomain.get({}):
            with suppress(ValueError):  # no snapshot with condition
                last_snapshot_cond, *_ = DeviceEventDomain.get(
                    {
                        '$query': {
                            'device': device['_id'],
                            'condition': {'$exists': True}
                        },
                        '$orderby': {'_created': pymongo.DESCENDING}
                    }
                )
                update = {'$set': {'condition': last_snapshot_cond['condition']}}
                DeviceDomain.update_one_raw(device['_id'], update)
