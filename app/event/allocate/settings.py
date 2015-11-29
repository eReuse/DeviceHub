import copy

from app.account.settings import unregistered_user
from app.event.settings import event_with_devices, event_sub_settings_multiple_devices

allocate = copy.deepcopy(event_with_devices)
allocate.update({
    'to': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
    },
    'unregisteredTo': {
        'type': 'dict',
        'schema': unregistered_user
    }
})
# Receiver OR ReceiverEmail. We need to hook this in a required field so it is always executed
# And @type is an always required field so we can happily hook on it

allocate_settings = copy.deepcopy(event_sub_settings_multiple_devices)
allocate_settings.update({
    'schema': allocate,
    'url': event_sub_settings_multiple_devices['url'] + 'allocate'
})
allocate_settings['datasource']['filter'] = {'@type': {'$eq': 'Allocate'}}
