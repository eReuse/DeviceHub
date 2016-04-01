import datetime

from app.resources.account.user import User
from app.rest import execute_post


def transfer_property(receives: list):
    for receive in receives:
        if receive['automaticallyAllocate']:
            a = execute_post('allocate', {
                '@type': 'Allocate',
                'to': receive['receiver'],
                'devices': receive['devices']
            })
            receive['_created'] = receive['_updated'] = a['_created'] + datetime.timedelta(milliseconds=1)


def set_organization(receives: list):
    """
    This method needs to execute after add_or_get_inactive_account
    :param receives:
    :return:
    """
    for receive in receives:
        org = User.get(receive['receiver']).get('organization')
        if org is not None:
            receive['receiverOrganization'] = org