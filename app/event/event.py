from app.utils import get_resource_name


class Event:
    @staticmethod
    def get_types() -> set:
        return Event.get_special_types() | Event.get_generic_types()

    @staticmethod
    def get_generic_types() -> set:
        return {'Ready', 'Repair', 'ToPrepare', 'ToRepair', 'ToRecycle', 'Recycle'}

    @staticmethod
    def get_special_types() -> set:
        return {'Add', 'Register', 'Snapshot', 'Remove', 'Receive', 'TestHardDrive', 'Allocate', 'Locate', 'Deallocate', 'EraseBasic'}  # Snapshot cannot be the last type

    @staticmethod
    def resource_types():
        return {get_resource_name(event) for event in Event.get_types()}
