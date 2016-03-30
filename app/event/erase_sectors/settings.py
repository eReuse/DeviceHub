import copy

from app.event.erase_basic.settings import EraseBasic
from app.event.settings import event_sub_settings_one_device, EventSubSettingsOneDevice

erase_sectors_settings = copy.deepcopy(event_sub_settings_one_device)


class EraseSectors(EraseBasic):
    pass

class EraseSectorsSettings(EventSubSettingsOneDevice):
    _schema = EraseSectors

