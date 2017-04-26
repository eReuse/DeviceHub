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


class EventNotFound(ResourceNotFound):
    pass
