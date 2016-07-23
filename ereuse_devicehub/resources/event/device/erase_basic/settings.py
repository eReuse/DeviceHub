from ereuse_devicehub.resources.event.device.settings import parent, EventWithOneDevice, EventSubSettingsOneDevice
from .step_settings import step


class EraseBasic(EventWithOneDevice):
    secureRandomSteps = {
        'type': 'natural',
        'required': True
    }
    endingTime = {
        'type': 'datetime'
    }
    startingTime = {
        'type': 'datetime'
    }
    success = {
        'type': 'boolean',
    }
    cleanWithZeros = {
        'type': 'boolean'
    }
    steps = {
        'type': 'list',  # OrderedSet
        'schema': {
            'type': 'dict',
            'schema': step
        }
    }
    parent = parent


class EraseBasicSettings(EventSubSettingsOneDevice):
    _schema = EraseBasic
