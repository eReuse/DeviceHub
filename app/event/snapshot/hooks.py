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
        app.data.driver.db.devices.update({'_id': test_hard_drives['device']}, {'$push': {'tests': test_hard_drives['_id']}})
