import copy

from app.event.settings import event_sub_settings_one_device, components, EventWithOneDevice, EventSubSettingsOneDevice


class Add(EventWithOneDevice):
    components = components


class AddSettings(EventSubSettingsOneDevice):
    _schema = Add

