from app.event.snapshot.snapshot import Snapshot
__author__ = 'Xavier Bustamante Talavera'


def pre_post_snapshot(request):
    snapshot = Snapshot(request.json['device'], request.json['components'])
    snapshot.prepare()
    request.json['events'] = [new_events['_id'] for new_events in snapshot.process()]
    request.json['device'] = request.json['device']['_id']
    request.json['components'] = [component['_id'] for component in request.json['components']]
