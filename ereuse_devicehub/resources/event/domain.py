from contextlib import suppress

from bson.objectid import ObjectId

from ereuse_devicehub.resources.domain import Domain, ResourceNotFound
from ereuse_devicehub.resources.event.device.settings import EventSettings


class EventDomain(Domain):
    resource_settings = EventSettings

    @classmethod
    def get_one(cls, id_or_filter: dict or ObjectId or str, **kwargs):
        try:
            return super().get_one(id_or_filter)
        except ResourceNotFound:
            raise EventNotFound()

    @classmethod
    def devices_id(cls, event: dict) -> list:
        """Gets a list of devices of the event, independently if they are in *device* or *devices* fields."""
        devices = event.get('devices', [])
        with suppress(KeyError):
            devices.append(event['device'])
        return devices


class EventNotFound(ResourceNotFound):
    pass
