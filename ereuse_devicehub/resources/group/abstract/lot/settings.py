from ereuse_devicehub.resources.group.abstract.lot.policy import Policies
from ereuse_devicehub.resources.group.abstract.settings import AbstractSettings, Abstract
from ereuse_devicehub.resources.group.settings import place_fk, lots_lots_fk, packages_fk, places_fk, lots_fk, \
    devices_fk


class Lot(Abstract):
    policies = {
        'type': 'dict',
        'schema': Policies()
    }
    ancestors = {
        'type': 'dict',
        'schema': {
            'places': place_fk,
            'lots': lots_lots_fk
        }
    }
    parents = {
        'type': 'dict',
        'schema': {
            'places': places_fk,
            'lots': lots_fk
        }
    }
    children = {
        'type': 'dict',
        'schema': {
            'packages': packages_fk,
            'lots': lots_fk,
            'devices': devices_fk
        }
    }


class LotSettings(AbstractSettings):
    _schema = Lot
    datasource = {
        'default_sort': [('_modified', -1)],
        'source': 'lots'
    }
    url = 'places'
