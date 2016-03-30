import copy

from app.event.settings import event_sub_settings_one_device, parent, EventWithOneDevice, EventSubSettingsOneDevice
from .step_settings import step

erase_basic_settings = copy.deepcopy(event_sub_settings_one_device)


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

class StepSettings(EventSubSettingsOneDevice):
    _schema = EraseBasic
