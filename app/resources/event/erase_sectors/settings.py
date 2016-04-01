import copy

from app.resources.event.erase_basic.settings import EraseBasic
from app.resources.event.settings import EventSubSettingsOneDevice


class EraseSectors(EraseBasic):
    pass

class EraseSectorsSettings(EventSubSettingsOneDevice):
    _schema = EraseSectors

