from bson import ObjectId
from flask import current_app

from app.utils import get_resource_name


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
        return Event.get_special_types() | Event.get_generic_types()

    @staticmethod
    def get_generic_types() -> set:
        return {'Ready', 'Repair', 'ToPrepare', 'ToRepair', 'ToRecycle', 'Recycle'}

    @staticmethod
    def get_special_types() -> set:
        return {'Add', 'Register', 'Snapshot', 'Remove', 'Receive', 'TestHardDrive', 'Allocate', 'Locate',
                'Deallocate', 'EraseBasic', 'EraseSectors'}  # Snapshot cannot be the last type

    @staticmethod
    def resource_types():
        return {get_resource_name(event) for event in Event.get_types()}


class EventNotFound(Exception):
    pass
