import copy

from app.event.settings import event_sub_settings_one_device, components, EventWithOneDevice, EventSubSettingsOneDevice


class Remove(EventWithOneDevice):
    components = components


class RemoveSettings(EventSubSettingsOneDevice):
    _schema = Remove

