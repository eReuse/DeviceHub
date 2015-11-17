import copy

from app.event.settings import event_with_one_device, event_sub_settings_one_device

register = copy.deepcopy(event_with_one_device)
register.update({
    'components': {  # We register the device AND its components, so this is writable
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'devices',
                'field': '_id',
                'embeddable': True
            }
        }
    }
})

register_settings = copy.deepcopy(event_sub_settings_one_device)
register_settings.update({
    'schema': register,
    'url': event_sub_settings_one_device['url'] + 'register'
})
register_settings['datasource']['filter'] = {'@type': {'$eq': 'Register'}}
