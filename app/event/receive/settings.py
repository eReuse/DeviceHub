import copy
from app.Validation import DEFAULT_AUTHOR

__author__ = 'Xavier Bustamante Talavera'
from app.event.settings import event_with_devices, event_sub_settings_multiple_devices

receive = copy.deepcopy(event_with_devices)
receive.update({
    'receiver': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True
        },
        'anyof': [{'required': True}, {'dependencies': ['receiverEmail']}]  # me OR email
    },
    'receiverEmail': {
        'type': 'string',
        'dependencies': ['receiverName']
    },
    'receiverName': {
        'type': 'string',
        'dependencies': ['receiverEmail']
    },
    'acceptedConditions': {
        'type': 'boolean',
        'required': True
    },
    'type': {
        'type': 'string',
        'required': True,
        'allowed': ['FinalUser', 'CollectionPoint', 'RecyclingPoint']
    }
})

receive_settings = copy.deepcopy(event_sub_settings_multiple_devices)
receive_settings.update({
    'schema': receive,
    #'url': event_sub_settings_multiple_devices['url'] + 'locate', todo choose url
    'url': 'events/receive'
})
receive_settings['datasource']['filter'] = {'@type': {'$eq': 'Receive'}}
