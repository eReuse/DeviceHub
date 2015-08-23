from app.Utils import get_resource_name

__author__ = 'busta'


class Event:
    @staticmethod
    def get_types() -> ():
        return 'Add', 'Register', 'Snapshot'

    @staticmethod
    def resource_types():
        return [get_resource_name(event) for event in Event.get_types()]
