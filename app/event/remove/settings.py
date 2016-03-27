import copy

from app.event.settings import event_with_one_device, event_sub_settings_one_device, components

remove = copy.deepcopy(event_with_one_device)
remove.update(copy.deepcopy(components))

remove_settings = copy.deepcopy(event_sub_settings_one_device)
remove_settings.update({
    'schema': remove
})
