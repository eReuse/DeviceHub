import pymongo

from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.validation.validation import HID_REGEX


class DeviceSettings(ResourceSettings):
    resource_methods = ['GET']
    item_methods = ['GET', 'PATCH']
    _schema = Device
    additional_lookup = {
        'field': 'hid',
        'url': 'regex("' + HID_REGEX + '")'
    }
    item_url = 'regex("[\w]+")'
    mongo_indexes = {
        '@type': [('@type', pymongo.DESCENDING)],
        '@type and subtype': [('@type', pymongo.DESCENDING), ('type', pymongo.DESCENDING)],
        '@type and _created': [('@type', pymongo.DESCENDING), ('_created', pymongo.DESCENDING)]
    }
    etag_ignore_fields = ['hid', '_id', 'components', 'isUidSecured', '_created', '_updated', '_etag', 'speed',
                          'busClock', 'labelId', 'owners', 'place', 'benchmark', 'benchmarks', 'public', '_links',
                          'forceCreation', 'parent', 'events']
    cache_control = 'max-age=1, must-revalidate'
    extra_response_fields = ResourceSettings.extra_response_fields + ['hid', 'pid']
    datasource = {
        'source': 'devices'
    }
    icon = 'devices/icons/'


class DeviceSubSettings(DeviceSettings):
    _schema = False
    resource_methods = ['GET']
    item_methods = []
