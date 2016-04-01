from ereuse_devicehub.resources.event.settings import components, EventWithOneDevice, EventSubSettingsOneDevice


class Add(EventWithOneDevice):
    components = components


class AddSettings(EventSubSettingsOneDevice):
    _schema = Add

