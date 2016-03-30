import copy

from app.event.erase_basic.settings import EraseBasic
from app.event.settings import EventSubSettingsOneDevice


class EraseSectors(EraseBasic):
    pass

class EraseSectorsSettings(EventSubSettingsOneDevice):
    _schema = EraseSectors

