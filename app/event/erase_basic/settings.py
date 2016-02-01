import copy

from app.event.settings import event_with_one_device, event_sub_settings_one_device
from .step_settings import step

erase_basic = copy.deepcopy(event_with_one_device)
erase_basic_settings = copy.deepcopy(event_sub_settings_one_device)
erase_basic.update({
    'secureRandomSteps': {
        'type': 'natural',
        'required': True
    },
    'endingTime': {
        'type': 'datetime'
    },
    'startingTime': {
        'type': 'datetime'
    },
    'success': {
        'type': 'boolean',
    },
    'cleanWithZeros': {
        'type': 'boolean'
    },
    'steps': {
        'type': 'list',  # OrderedSet
        'schema': {
            'type': 'dict',
            'schema': step
        }
    }
})
erase_basic_settings.update({
    'schema': erase_basic,
    'url': event_sub_settings_one_device['url'] + 'erase_basic'
})
erase_basic_settings['datasource']['filter'] = {'@type': {'$eq': 'EraseBasic'}}
