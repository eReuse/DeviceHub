from flask import request
from .snapshot import Snapshot


def on_insert_snapshot(items):
    for item in items:
        snapshot = Snapshot(item['device'], item['components'])
        snapshot.prepare()
        item['events'] = [new_events['_id'] for new_events in snapshot.process()]
        item['device'] = item['device']['_id']
        item['components'] = [component['_id'] for component in item['components']]
        item['unsecured'] = [device['_id'] for device in snapshot.unsecured]

def save_request(items):
    """S
    Saves the original request in a string in the 'request' field in json for debugging purposes.

    Warning: This method does not support bulk inserts.
    """
    items[0]['request'] = request.data.decode()
