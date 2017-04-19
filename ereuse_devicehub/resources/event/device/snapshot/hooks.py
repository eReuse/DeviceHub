from contextlib import suppress

from flask import current_app as app
from flask import request, g
from werkzeug.local import LocalProxy

from ereuse_devicehub.exceptions import InnerRequestError
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.domain import EventNotFound
from ereuse_devicehub.rest import execute_delete
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
    app.data.driver.db.devices.update({'_id': event['device']}, {'$push': {field_name: event['_id']}})


def set_secured(snapshots: list):
    """
    Sets secured param in a snapshot if this was signed.
    :param snapshots:
    :return:
    """
    for snapshot in snapshots:
        snapshot['secured'] = g.trusted_json


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
    if '_id' in payload.json:
        payload.json['device']['_id'] = payload.json.pop('_id')
    if 'pid' in payload.json:  # todo workbench hotfix for pid
        payload.json['device']['pid'] = payload.json.pop('pid')
    if payload.json.get('snapshotSoftware', None) in SNAPSHOT_SOFTWARE:
        payload.json['snapshotSoftware'] = SNAPSHOT_SOFTWARE[payload.json['snapshotSoftware']]
