import copy

from ereuse_devicehub.resources.event.erase_basic.settings import EraseBasic
from ereuse_devicehub.resources.event.settings import EventSubSettingsOneDevice


class EraseSectors(EraseBasic):
    pass

class EraseSectorsSettings(EventSubSettingsOneDevice):
    _schema = EraseSectors

