import copy

from app.device.component.settings import component
from app.device.settings import device
from app.event.settings import event_with_one_device, event_sub_settings_one_device

register = copy.deepcopy(event_with_one_device)
register.update({
    'device': {
        'type': 'dict',
        'schema': device  # anyof causes a bug where resource is not set
    },
    'components': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': component
        },
        'default': []
    },
})

register_settings = copy.deepcopy(event_sub_settings_one_device)
register_settings.update({
    'resource_methods': ['POST'],
    'schema': register,
    'url': event_sub_settings_one_device['url'] + 'register',
    'extra_response_fields': ['device', 'components']
})
register_settings['datasource']['filter'] = {'@type': {'$eq': 'Register'}}
