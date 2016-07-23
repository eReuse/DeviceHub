from ereuse_devicehub.resources.event.device.settings import components, EventWithOneDevice, EventSubSettingsOneDevice


class Remove(EventWithOneDevice):
    components = components


class RemoveSettings(EventSubSettingsOneDevice):
    _schema = Remove
