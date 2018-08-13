from ereuse_devicehub.resources.event.device.settings import EventSubSettingsMultipleDevices, EventWithDevices


class Update(EventWithDevices):
    margin = {
        'type': 'string'
    }
    price = {
        'type': 'string'
    }
    partners = {
        'type': 'string'
    }
    originNote = {
        'type': 'string'
    }
    targetNote = {
        'type': 'string'
    }
    maintenance = {
        'type': 'boolean'
    }
    guaranteeYears = {
        'type': 'natural'
    }


class UpdateSettings(EventSubSettingsMultipleDevices):
    _schema = Update
    fa = 'fa-pencil'
    short_description = 'Internal use only.'
