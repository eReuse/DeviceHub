from ereuse_devicehub.resources.event.device.settings import parent_materialized, EventWithOneDevice, \
    EventSubSettingsOneDevice

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
    parent = parent_materialized


class EraseBasicSettings(EventSubSettingsOneDevice):
    _schema = EraseBasic
    fa = 'fa-eraser'
    short_description = 'Fast erasure of the HardDrive'
    item_methods = ['GET']
