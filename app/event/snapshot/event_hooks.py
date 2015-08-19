from .snapshot import Snapshot
__author__ = 'Xavier Bustamante Talavera'


def on_insert_snapshot(items):
    for item in items:
        snapshot = Snapshot(item['device'], item['components'])
        snapshot.prepare()
        item['events'] = [new_events['_id'] for new_events in snapshot.process()]
        item['device'] = item['device']['_id']
        item['components'] = [component['_id'] for component in item['components']]
