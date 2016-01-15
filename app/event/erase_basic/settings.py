import copy

from app.event.settings import event_with_one_device, event_sub_settings_one_device
from app.validation import IF_VALUE_REQUIRE

erase_basic = copy.deepcopy(event_with_one_device)
erase_basic_settings = copy.deepcopy(event_sub_settings_one_device)
erase_basic.update({
    'secureAleatorySteps': {
        'type': 'natural',
        'required': True
    },
    'elapsedTime': {
        'type': 'datetime',
    },
    'endTime': {
        'type': 'datetime'
    },
    'startTime': {
        'type': 'datetime'
    },
    'state': {
        'type': 'string',
        'allowed': ['success', 'fail'],
    },
    'cleanWithZeros': {
        'type': 'boolean'
    }
})
erase_basic_settings.update({
    'schema': erase_basic,
    'url': event_sub_settings_one_device['url'] + 'erase_basic'
})
erase_basic_settings['datasource']['filter'] = {'@type': {'$eq': 'EraseBasic'}}
