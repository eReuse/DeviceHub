from contextlib import suppress
from typing import List

from flask import g, request
from werkzeug.local import LocalProxy

from ereuse_devicehub.exceptions import InnerRequestError, SchemaError
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.domain import ResourceNotFound
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.domain import EventNotFound
from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.rest import execute_delete, execute_patch
from ereuse_devicehub.utils import Naming
from .snapshot import Snapshot, SnapshotWithoutComponents


def on_insert_snapshot(items):
    for item in items:
        if 'label' in item:
            item['device']['labelId'] = item['label']  # todo as we do not update the values of a device,
        # todo we will never update, thus materializing new label ids
        if item['snapshotSoftware'] == 'Workbench':
            snapshot = Snapshot(item['device'], item['components'], item.get('created'), item.get('parent'))
        else:  # In App or web we do not ask for component info
            snapshot = SnapshotWithoutComponents(item['device'], created=item.get('created'), parent=item.get('parent'))
        item['events'] = [new_events['_id'] for new_events in snapshot.execute()]
        item['device'] = snapshot.device['_id']
        item['components'] = [component['_id'] for component in snapshot.components]
        item['unsecured'] = snapshot.unsecured
        from ereuse_devicehub.resources.hooks import set_date
        set_date(None, items)  # Let's get the time AFTER creating the other events


def save_request(items):
    """
    Saves the original request in a string in the 'request' field in json for debugging purposes.

    Warning: This method does not support bulk inserts.
    """
    items[0]['request'] = request.data.decode()


def materialize_test_hard_drives(_):
    for i, test_hard_drives in getattr(g, 'snapshot_test_hard_drives', []):
        _materialize_event_in_device(test_hard_drives, 'tests')


def materialize_erase_basic(_):
    for i, erase_basic in getattr(g, 'snapshot_basic_erasures', []):
        _materialize_event_in_device(erase_basic, 'erasures')


def _materialize_event_in_device(event, field_name):
    DeviceDomain.update_one_raw(event['device'], {'$push': {field_name: event['_id']}})


def materialize_condition(snapshots: list):
    """Materializes condition of devices after successful snapshot"""
    for snapshot in snapshots:
        if 'condition' in snapshot:
            DeviceDomain.update_one_raw(snapshot['device'], {'$set': {'condition': snapshot['condition']}})


def set_secured(snapshots: list):
    """
    Sets secured param in a snapshot if this was signed.
    :param snapshots:
    :return:
    """
    for snapshot in snapshots:
        snapshot['secured'] = g.get('trusted_json', False)


def delete_events(_, snapshot: dict):
    """Deletes the events that were created with the snapshot."""
    if snapshot.get('@type') == 'devices:Snapshot':
        for event_id in snapshot['events']:
            with suppress(EventNotFound):
                # If the first event is Register, erasing the device will erase the rest of events
                event = DeviceEventDomain.get_one(event_id)
                try:
                    execute_delete(Naming.resource(event['@type']), event['_id'])
                except InnerRequestError as e:
                    if e.status_code != 404:
                        raise e


SNAPSHOT_SOFTWARE = {
    'DDI': 'Workbench',
    'Scan': 'AndroidApp',
    'DeviceHubClient': 'Web'
}


def move_id(payload: LocalProxy):
    """Moves the _id and pid from the snapshot to the inner device of the snapshot, as a hotfix for Workbench's bug"""
    snapshot = payload.get_json()
    if '_id' in snapshot:
        snapshot['device']['_id'] = snapshot.pop('_id')
    if 'pid' in snapshot:  # todo workbench hotfix for pid
        snapshot['device']['pid'] = snapshot.pop('pid')
    if snapshot.get('snapshotSoftware', None) in SNAPSHOT_SOFTWARE:
        snapshot['snapshotSoftware'] = SNAPSHOT_SOFTWARE[snapshot['snapshotSoftware']]


def add_to_group(snapshots: List[dict]):
    """Adds the device to the group, if it was not there before."""
    for snapshot in snapshots:
        if 'group' in snapshot:
            try:
                g_type = snapshot['group']['@type']
                resource_name = Naming.resource(g_type)
                group = GroupDomain.children_resources[resource_name].get_one(snapshot['group']['_id'])
                # We add the device in the group if it didn't exist already
                if snapshot['device'] not in group['children'].get('devices', []):
                    group['children'].setdefault('devices', []).append(snapshot['device'])
                    group_patch = {'@type': g_type, 'children': group['children']}
                    execute_patch(resource_name, group_patch, group['_id'])
            except (ResourceNotFound, InnerRequestError) as e:
                raise SchemaError(field='group',
                                  message='We created the Snapshot, but we couldn\'t add '
                                          'the devices to the group {} because {}'
                                  .format(snapshot['group']['_id'], e)) from e
