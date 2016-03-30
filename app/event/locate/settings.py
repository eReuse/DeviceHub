import copy

from app.event.settings import event_sub_settings_multiple_devices, place, components, EventWithDevices, \
    EventSubSettingsMultipleDevices


class Locate(EventWithDevices):
    place = place
    components = copy.deepcopy(components)

Locate.components['readonly'] = True
Locate.geo = copy.deepcopy(Locate.geo)
Locate.geo['excludes'] = 'place'  # geo xor place
Locate.geo['or'] = ['place']


class LocateSettings(EventSubSettingsMultipleDevices):
    _schema = Locate
