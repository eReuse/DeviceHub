import pprint
from app.event.snapshot.snapshot import Snapshot

__author__ = 'Xavier Bustamante Talavera'


def pre_get_snapshot(request, lookup):
    pprint.pprint("hi")


def pre_post_snapshot(request):
    snapshot = Snapshot(request.json)
    snapshot.prepare()
    snapshot.execute_all()
    request.json['device'] = request.json['device']['_id']
    _ids = []
    for component in request.json['components']:
        _ids.append(component['_id'])
    request.json['components'] = _ids


