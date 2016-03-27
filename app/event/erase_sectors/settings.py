import copy

from app.event.erase_basic.settings import erase_basic
from app.event.settings import event_sub_settings_one_device

erase_sectors = copy.deepcopy(erase_basic)
erase_sectors_settings = copy.deepcopy(event_sub_settings_one_device)

erase_sectors_settings.update({
    'schema': erase_sectors
})
