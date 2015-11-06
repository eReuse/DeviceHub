import copy

__author__ = 'Xavier Bustamante Talavera'
from app.event.settings import event_with_one_device, event_sub_settings_one_device

add = copy.deepcopy(event_with_one_device)
add_settings = copy.deepcopy(event_sub_settings_one_device)
add.update({
    'components': {
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
add_settings.update({
    'schema': add,
    'url': event_sub_settings_one_device['url'] + 'add'
})
add_settings['datasource']['filter'] = {'@type': {'$eq': 'Add'}}
