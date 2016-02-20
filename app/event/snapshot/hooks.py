from flask import request, g

from app.app import app
from .snapshot import Snapshot


def on_insert_snapshot(items):
    for item in items:
        if 'label' in item:
            item['device']['labelId'] = item['label']  # todo as we do not update the values of a device,
        # todo we will never udpate, thus materializing new label ids
        snapshot = Snapshot(item['device'], item['components'])
        item['events'] = [new_events['_id'] for new_events in snapshot.execute()]
        item['device'] = item['device']['_id']
        item['components'] = [component['_id'] for component in item['components']]
        item['unsecured'] = snapshot.unsecured


def save_request(items):
    """
    Saves the original request in a string in the 'request' field in json for debugging purposes.

    Warning: This method does not support bulk inserts.
    """
    items[0]['request'] = request.data.decode()


def materialize_test_hard_drives(snapshots: list):
    for i, test_hard_drives in g.snapshot_test_hard_drives:
        _materialize_event_in_device(test_hard_drives, 'tests')


def materialize_erase_basic(snapshots: list):
    for i, erase_basic in g.snapshot_basic_erasures:
        _materialize_event_in_device(erase_basic, 'erasures')


def _materialize_event_in_device(event, field_name):
    app.data.driver.db.devices.update({'_id': event['device']}, {'$push': {field_name: event['_id']}})
