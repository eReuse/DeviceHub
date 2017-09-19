import copy

from ereuse_devicehub.resources.event.device.settings import place, EventWithDevices, \
    EventSubSettingsMultipleDevices, materialized_components


class Locate(EventWithDevices):
    place = place
    components = materialized_components


Locate.geo = copy.deepcopy(Locate.geo)
Locate.geo['excludes'] = 'place'  # geo xor place
Locate.geo['or'] = ['place']


class LocateSettings(EventSubSettingsMultipleDevices):
    _schema = Locate
    fa = 'fa-map-marker'
    sink = -3
    short_description = 'The devices have been placed.'
