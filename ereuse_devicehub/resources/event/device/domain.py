import pymongo
from ereuse_devicehub.resources.event.domain import EventDomain
from ereuse_devicehub.utils import Naming


class DeviceEventDomain(EventDomain):
    GENERIC_TYPES = {
        'Ready': {
            'fa': 'fa-check',
            'short_description': 'The devices work correctly, so they are ready to be used, sold, donated...',
            'sink': -2
        },
        'Repair': {
            'fa': 'fa-chain-broken',
            'short_description': 'The devices have been succesfully repaired',
            'sink': -1
        },
        'ToPrepare': {
            'fa': 'fa-wrench',
            'short_description': 'The devices need some maintenance, some kind of testing or preparation... to be ready',
            'sink': 1
        },
        'ToRepair': {
            'fa': 'fa-chain-broken',
            'short_description': 'The devices need repairing',
            'sink': 0
        },
        'ToDispose': {
            'fa': 'fa-trash-o',
            'short_description': 'The devices need to be taken for disposal.',
            'sink': -8
        },
        'Dispose': {
            'fa': 'fa-trash-o',
            'short_description': 'The devices have been successfully taken for disposal.',
            'sink': -9
        },
        'Free': {
            'fa': 'fa-shopping-cart',
            'short_description': 'The devices are available to be received for someone (sold, donated)',
            'sink': -4
        }
    }

    @staticmethod
    def add_prefix(type_name: str) -> str:
        """
        Adds a prefix to the type of a DeviceEvent (or subclass), if needed, and returns the full type with the prefix.

        It is used as coerce in @type field of DeviceEvent.
        """
        from ereuse_devicehub.resources.event.device.settings import DeviceEvent
        if type_name in (subclass.__name__ for subclass in DeviceEvent.subclasses()):
            return DeviceEventDomain.new_type(type_name)
        else:
            return str(type_name)

    @staticmethod
    def new_type(type_name):
        from ereuse_devicehub.resources.event.device.settings import DeviceEvent
        return Naming.new_type(type_name, DeviceEvent._settings['prefix'])

    @staticmethod
    def get_first_snapshot(device_id: str):
        return DeviceEventDomain.get_one(
            {'$query': {'device': device_id, '@type': 'devices:Snapshot'}, '$orderby': {'_created': pymongo.ASCENDING}})
