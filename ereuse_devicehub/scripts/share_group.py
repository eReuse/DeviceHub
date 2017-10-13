import argparse
import json

from ereuse_devicehub import DeviceHub
from ereuse_devicehub.resources.group.settings import Group
from ereuse_devicehub.security.perms import READ
from ereuse_devicehub.tests import Client
from ereuse_devicehub.utils import Naming
from pydash import find


def share_group(app: DeviceHub, email: str, password: str, group_type: str, receiver_email: str, perm=READ,
                group_id: str = None, group_label=None, db: str = None):
    """
    Sets the permission for the user in the group, known as sharing. If the user had an existing permission,
    this is replaced.

    If you want to execute it through the console, see the next function ``main()``.

    :param email: Email of the person sharing the group.
    :param password: Password of the person sharing the group.
    :param app: DeviceHub app, needed for the configs (database info, etc).
    :param group_type: Ex: ``Lot``.
    :param receiver_email: The e-mail of the user to share the group to.
    :param perm:
    :param group_id: Optional. The identifier of the group. Name xor group id needed.
    :param group_label: Optional. The name of the group. Name xor group id needed.
    :param db: The database where the group is in.
    """
    if not group_id and not group_label:
        raise ValueError('Group name xor group_id needed.')
    if group_type not in Group.types:
        raise ValueError('Group type should be one of {}'.format(Group.types))
    c = Client(app=app)
    c.prepare()
    token = c.login(email, password)['token']
    kwargs = {'token': token, 'db': db}
    if group_label:
        kwargs['params'] = {'where': json.dumps({'label': group_label})}
    else:
        kwargs['item'] = group_id
    response = c.get_200(Naming.resource(group_type), **kwargs)
    group = response['_items'][0] if group_label else response
    account_params = {'where': json.dumps({'email': receiver_email})}
    receiver = c.get_200(c.ACCOUNTS, params=account_params, token=token)['_items'][0]
    existing_perm = find(group.setdefault('perms', []), {'_id': receiver['_id']})
    if existing_perm:
        existing_perm['perm'] = perm
    else:
        group['perms'].append({'account': receiver['_id'], 'perm': perm})
    group_patch = {'@type': group_type, 'perms': group['perms']}
    return c.patch_200(Naming.resource(group_type), item=group['_id'], data=group_patch, token=token, db=db)


def main(app):
    """
    Create a python file with the following contents::

        from app import app  # Where your ``DeviceHub()`` is defined
        from ereuse_devicehub.scripts.share_group import main
        main(app)

    And execute it.
    """
    desc = 'Share a group.'
    epilog = 'Minimum example: python share_group.py a@a.a 1234 Lot b@b.b -i identifier'
    parser = argparse.ArgumentParser(description=desc, epilog=epilog)
    parser.add_argument('email', help='The email of the person sharing this.')
    parser.add_argument('password', help='The password of the person sharing this.')
    parser.add_argument('group_type')
    parser.add_argument('receiver_email', help='The email of the user that this is being shared to.')
    parser.add_argument('-i', '--group_id', help='The group id.')
    parser.add_argument('-l', '--group_label', help='The group name. If set, this is used over the id. '
                                                   'Note that names are not unique, use the id when possible.')
    # We need to set default or this will be ``None``
    parser.add_argument('-p', '--perm', help='The permission the user will have. READ by default.', default=READ)
    parser.add_argument('-d', '--db', help='The database of the group. Otherwise the default database of the user.')
    args = vars(parser.parse_args())
    response = share_group(app, **args)
    print('Response:')
    print(json.dumps(response, indent=4))
