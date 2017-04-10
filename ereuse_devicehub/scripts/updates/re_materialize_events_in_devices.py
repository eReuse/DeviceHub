import pymongo

from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.hooks import MaterializeEvents
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.scripts.updates.update import Update
from ereuse_devicehub.utils import Naming


class ReMaterializeEventsInDevices(Update):
    """
    Re-computes the *events* field in the devices. Note that events usually materialize *components* in devices and
    *parent* in components, which are **not rematerialized here**.
    """
    def execute(self, database):
        DeviceDomain.update_many_raw({}, {'$set': {'events': []}})
        for event in DeviceEventDomain.get({'$query': {}, '$orderby': {'_created': pymongo.ASCENDING}}):
            MaterializeEvents.materialize_events(Naming.resource(event['@type']), [event])
