from app.utils import get_resource_name


class Event:
    @staticmethod
    def get_types() -> ():
        return 'Add', 'Register', 'Snapshot', 'Remove', 'Receive', 'TestHardDrive', 'Allocate', 'Locate'  # Snapshot cannot be the last type

    @staticmethod
    def resource_types():
        return [get_resource_name(event) for event in Event.get_types()]
