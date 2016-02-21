import copy

from app.event.settings import event_with_devices, event_sub_settings_multiple_devices, components

deallocate = copy.deepcopy(event_with_devices)
deallocate.update({
    'from': {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
        'sink': 2
    },
    'fromOrganization': {  # Materialization of the organization that, by the time of the deallocation, the user worked in
        'type': 'string',
        'readonly': True
    }
})
deallocate.update(copy.deepcopy(components))
deallocate['components']['readonly'] = True

# Receiver OR ReceiverEmail. We need to hook this in a required field so it is always executed
# And @type is an always required field so we can happily hook on it

deallocate_settings = copy.deepcopy(event_sub_settings_multiple_devices)
deallocate_settings.update({
    'schema': deallocate,
    'url': event_sub_settings_multiple_devices['url'] + 'deallocate'
})
deallocate_settings['datasource']['filter'] = {'@type': {'$eq': 'Deallocate'}}
