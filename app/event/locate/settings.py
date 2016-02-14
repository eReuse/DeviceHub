import copy

from app.event.settings import event_with_devices, event_sub_settings_multiple_devices, place, components

locate = copy.deepcopy(event_with_devices)
locate.update(copy.deepcopy(place))
locate.update(copy.deepcopy(components))
locate['components']['readonly'] = True

locate['geo']['excludes'] = 'place'  # geo xor place
locate['geo']['or'] = ['place']

locate_settings = copy.deepcopy(event_sub_settings_multiple_devices)
locate_settings.update({
    'schema': locate,
    # 'url': event_sub_settings_multiple_devices['url'] + 'locate',
    'url': 'events/locate'
})
locate_settings['datasource']['filter'] = {'@type': {'$eq': 'Locate'}}
