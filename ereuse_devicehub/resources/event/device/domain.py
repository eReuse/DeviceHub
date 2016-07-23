from ereuse_devicehub.resources.event.domain import EventDomain
from ereuse_devicehub.utils import Naming


class DeviceEventDomain(EventDomain):
    GENERIC_TYPES = {'Ready', 'Repair', 'ToPrepare', 'ToRepair', 'ToDispose', 'Dispose', 'Free'}

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