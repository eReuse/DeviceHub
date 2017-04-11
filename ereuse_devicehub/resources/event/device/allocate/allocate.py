import pymongo
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.allocate.hooks import materialize_actual_owners_add
from ereuse_devicehub.resources.event.device.deallocate.hooks import materialize_actual_owners_remove


def materialize_owners(devices_id):
    """Re-computes 'owners' for the given devices and components."""
    # First let's erase all owners
    DeviceDomain.update_many_raw({'_id': {'$in': devices_id}}, {'$set': {'owners': []}})
    # Then let's execute again the materialize hooks for Allocate/Deallocate
    query = {'$or': [{'@type': 'devices:Allocate'}, {'@type': 'devices:Deallocate'}], 'devices': {'$in': devices_id}}
    order_by = {'_created': pymongo.ASCENDING}
    for event in DeviceEventDomain.get({'$query': query, '$orderby': order_by}):
        if event['@type'] == 'devices:Allocate':
            materialize_actual_owners_add([event])
        else:
            modified = materialize_actual_owners_remove([event])
            if modified == 0:  # This Remove does nothing and should be erased
                DeviceEventDomain.delete_one({'_id': event['_id']})
