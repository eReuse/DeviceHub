from contextlib import suppress

from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.domain import EventNotFound
from ereuse_devicehub.resources.group.physical.place.domain import CannotDeleteIfHasEvent


def avoid_deleting_if_has_event(item):
    with suppress(EventNotFound):
        DeviceEventDomain.get_one({'place': item['_id']})
        raise CannotDeleteIfHasEvent()
