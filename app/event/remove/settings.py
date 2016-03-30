from app.event.settings import components, EventWithOneDevice, EventSubSettingsOneDevice


class Remove(EventWithOneDevice):
    components = components


class RemoveSettings(EventSubSettingsOneDevice):
    _schema = Remove

