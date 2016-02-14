import copy

from app.event.settings import event_with_one_device, event_sub_settings_one_device, components

add = copy.deepcopy(event_with_one_device)
add_settings = copy.deepcopy(event_sub_settings_one_device)
add.update(copy.deepcopy(components))
add_settings.update({
    'schema': add,
    'url': event_sub_settings_one_device['url'] + 'add'
})
add_settings['datasource']['filter'] = {'@type': {'$eq': 'Add'}}
