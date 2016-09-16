import copy

from ereuse_devicehub.resources.event.device.settings import place, components, EventWithDevices, \
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
    fa = 'fa-map-marker'
    short_description = 'The devices have been placed.'
