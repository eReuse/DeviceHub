import copy

from ereuse_devicehub.resources.group.physical.settings import Physical, PhysicalSettings
from ereuse_devicehub.resources.group.settings import groups, place_fk, lots_lots_fk, packages_fk, places_fk, lots_fk, \
    package_fk, devices_fk
from ereuse_devicehub.resources.schema import Thing, UnitCodes


class Package(Physical):
    weight = {
        'type': 'float',
        'unitCode': UnitCodes.kgm,
        'sink': -1,
        'teaser': False
    }
    width = {
        'type': 'float',
        'unitCode': UnitCodes.m,
        'sink': -1,
        'teaser': False
    }
    height = {
        'type': 'float',
        'unitCode': UnitCodes.m,
        'sink': -1,
        'teaser': False
    }
    depth = {
        'type': 'float',
        'unitCode': UnitCodes.m,
        'sink': -1,
        'teaser': False
    }
    ancestors = {
        'type': 'dict',
        'schema': {
            'places': place_fk,
            'lots': lots_lots_fk,
            'packages': packages_fk
        }
    }
    parents = {
        'type': 'dict',
        'schema': {
            'places': places_fk,
            'lots': lots_fk,
            'packages': package_fk
        }
    }
    children = {
        'type': 'dict',
        'schema': {
            'packages': packages_fk,
            'devices': devices_fk
        }
    }

class PackageSettings(PhysicalSettings):
    resource_methods = ['GET', 'POST']
    item_methods = ['GET', 'PATCH', 'DELETE', 'PUT']
    _schema = Package
    datasource = {
        'default_sort': [('_modified', -1)],
        'source': 'packages'
    }
    url = 'packages'
