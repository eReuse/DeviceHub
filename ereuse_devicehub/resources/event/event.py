from bson import ObjectId
from flask import current_app

from ereuse_devicehub.utils import Naming


class Event:
    @staticmethod
    def get_one(id_or_query: dict or ObjectId or str):
        """

        :param id_or_query:
        :raises EventNotFound:
        :return:
        """
        event = current_app.data.find_one_raw('events', id_or_query)
        if event is None:
            raise EventNotFound
        else:
            return event

    @staticmethod
    def get(query: dict):
        return list(current_app.data.find_raw('events', query))

    @staticmethod
    def get_types() -> set:
        # todo is it dangerous to return EventWithOneDevice and EventWithDevices?
        from .settings import Event as EventSchema
        from ereuse_devicehub.resources.event.settings import EventWithOneDevice
        from ereuse_devicehub.resources.event import EventWithDevices
        remove = (EventWithOneDevice, EventWithDevices)
        return {cls.__name__ for cls in EventSchema.subclasses() if cls not in remove}

    @staticmethod
    def get_generic_types() -> set:
        return {'Ready', 'Repair', 'ToPrepare', 'ToRepair', 'ToDispose', 'Dispose', 'Free'}

    @staticmethod
    def get_special_types() -> set:
        return {'Add', 'Register', 'Snapshot', 'Remove', 'Receive', 'TestHardDrive', 'Allocate', 'Locate',
                'Deallocate', 'EraseBasic', 'EraseSectors'}  # Snapshot cannot be the last type

    @staticmethod
    def resource_types():
        return {Naming.resource(event) for event in Event.get_types()}


class EventNotFound(Exception):
    pass
