import json
from argparse import ArgumentParser
from getpass import getpass
from uuid import uuid4

from bson import ObjectId

from ereuse_devicehub import DeviceHub
from ereuse_devicehub.tests import Client


def duplicate_snapshot(app: DeviceHub,
                       email: str,
                       password: str,
                       snapshot_id: ObjectId,
                       db: str = None):
    """
    Makes a totally new snapshot from the data of an existing a snapshot.

    It uploads an exact copy of the snapshot but changing the uuid.
    """
    c = Client(app=app)
    c.prepare()
    account = c.login(email, password)
    db = db or account['defaultDatabase']
    snapshot = c.get_200(c.EVENTS, item=str(snapshot_id), token=account['token'], db=db)
    assert snapshot['@type'] == 'devices:Snapshot'
    snapshot = json.loads(snapshot['request'])
    snapshot['_uuid'] = uuid4()
    return c.post_201(c.DEVICE_EVENT_SNAPSHOT, data=snapshot, token=account['token'], db=db)


def main(app: DeviceHub):
    epilog = 'Minimum example: python duplicate_snapshot.py a@a.a ﻿5ae03bf3c346b8898b1f2c9e'
    parser = ArgumentParser(description=duplicate_snapshot.__doc__, epilog=epilog)
    parser.add_argument('email', help='The email of the author of this new snapshot.')
    parser.add_argument('snapshot_id', help='The ID of the snapshot', type=ObjectId)
    parser.add_argument('-d', '--db',
                        help='The database of the group. If empty, we use the user\'s default.',
                        choices=app.config['DATABASES'])
    args = vars(parser.parse_args())
    args['password'] = getpass('Enter {} password: '.format(args['email']))
    response = duplicate_snapshot(app, **args)
    print('Response:')
    print(json.dumps(response, indent=4))
