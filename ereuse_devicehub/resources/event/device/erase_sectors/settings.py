from ereuse_devicehub.resources.event.device.erase_basic.settings import EraseBasic
from ereuse_devicehub.resources.event.device.settings import EventSubSettingsOneDevice


class EraseSectors(EraseBasic):
    pass


class EraseSectorsSettings(EventSubSettingsOneDevice):
    _schema = EraseSectors
    fa = 'fa-eraser'