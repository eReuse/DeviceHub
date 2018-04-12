import json
import warnings
from argparse import ArgumentParser
from getpass import getpass
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from PIL import Image

from ereuse_devicehub import DeviceHub
from ereuse_devicehub.tests import Client


def snapshot_pictures(app: DeviceHub, email: str, password: str, device_id: str,
                      pic_dir: Path, db: str = None):
    """Add pictures to a computer by creating a new Snapshot."""
    c = Client(app=app)
    c.prepare()
    account = c.login(email, password)
    db = db or account['defaultDatabase']
    device = c.get_200(c.DEVICES, item=device_id, token=account['token'], db=db)
    snapshot = {
        '_uuid': str(uuid4()),
        '@type': 'devices:Snapshot',
        'snapshotSoftware': 'Photobox',
        'version': '0.0.1',
        'device': {'_id': device_id, '@type': device['@type']},
        'picture_info': {
            'software': 'Pbx',
            'version': '0.0.1'
        }
    }
    snapshot = {k: json.dumps(v) for k, v in snapshot.items()}
    snapshot['pictures'] = []
    warnings.simplefilter('error', Image.DecompressionBombWarning)  # Throw security error
    for path in pic_dir.iterdir():
        pic = Image.open(path)  # type: Image
        try:
            pic.thumbnail(size=(1600, 1600))
            bytes = BytesIO()
            pic.save(bytes, 'JPEG', quality=80, optimize=True, progressive=True)
            bytes.seek(0)  # Reset position of the bytes array
            snapshot['pictures'].append((bytes, path.name))
        finally:
            pic.close()

    snapshot = c.post_201(c.DEVICE_EVENT_SNAPSHOT, snapshot,
                          content_type='multipart/form-data',
                          token=account['token'],
                          db=db)
    # Ensure we can get a picture
    c.get_200(snapshot['pictures'][0]['file'][1:], token=account['token'], db=db)
    print('Uploaded picture paths:')
    print(*['{}{}'.format(db, p['file']) for p in snapshot['pictures']], sep='\n')


def main(app: DeviceHub):
    epilog = 'Minimum example: python snapshot_pictures.py a@a.a 123 /path/to/pics/folder/'
    parser = ArgumentParser(description=snapshot_pictures.__doc__, epilog=epilog)
    parser.add_argument('email', help='The email of the person sharing this.')
    parser.add_argument('device_id', help='The ID of the device.')
    parser.add_argument('pic_dir',
                        type=Path,
                        help='A path to the folder containing the pictures. '
                             'Pictures must be named like 1.jpg, 2.jpg...')
    parser.add_argument('-d', '--db',
                        help='The database of the group. If empty, we use the user default.',
                        choices=app.config['DATABASES'])
    args = vars(parser.parse_args())
    args['password'] = getpass('Enter {} password: '.format(args['email']))
    response = snapshot_pictures(app, **args)
    print('Response:')
    print(json.dumps(response, indent=4))
