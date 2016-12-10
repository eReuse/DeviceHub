import datetime
from contextlib import suppress

from ereuse_devicehub.resources.account.domain import AccountDomain, UserNotFound
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.rest import execute_post_internal
from ereuse_devicehub.utils import Naming


def transfer_property(receives: list):
    for receive in receives:
        if receive['automaticallyAllocate']:
            allocate_type = DeviceEventDomain.new_type('Allocate')
            a = execute_post_internal(Naming.resource(allocate_type), {
                '@type': allocate_type,
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
        with suppress(UserNotFound):
            receive['receiverOrganization'] = AccountDomain.get_one(receive['receiver']).get('organization')
