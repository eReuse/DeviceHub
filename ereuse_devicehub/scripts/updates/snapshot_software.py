from contextlib import suppress

from pydash import find

from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.scripts.updates.update import Update


class SnapshotSoftware(Update):
    """
    Changes the values of SnapshotSoftware and adds it to the materialized one in devices
    """

    def execute(self, database):
        SNAPSHOT_SOFTWARE = {
            'DDI': 'Workbench',
            'Scan': 'AndroidApp',
            'DeviceHubClient': 'Web'
        }
        for snapshot in DeviceEventDomain.get({'@type': "devices:Snapshot"}):
            with suppress(KeyError):
                snapshot['snapshotSoftware'] = SNAPSHOT_SOFTWARE[snapshot.get('snapshotSoftware', 'DDI')]
            DeviceEventDomain.update_one_raw(snapshot['_id'], {'$set': {'snapshotSoftware': snapshot['snapshotSoftware']}})
            for device in DeviceDomain.get({'events._id': snapshot['_id']}):
                materialized_snapshot = find(device['events'], lambda event: event['_id'] == snapshot['_id'])
                materialized_snapshot['snapshotSoftware'] = snapshot['snapshotSoftware']
                DeviceDomain.update_one_raw(device['_id'], {'$set': {'events': device['events']}})
