import pymongo

from app.resources.device.schema import Device
from app.resources.resource import ResourceSettings
from app.validation import HID_REGEX


class DeviceSettings(ResourceSettings):
    resource_methods = ['GET', 'POST']
    item_methods = ['GET', 'PATCH']  # todo patch should only be able to modify selected fields like public
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
    etag_ignore_fields = ['hid', '_id', 'components', 'isUidSecured', '_created', '_updated', '_etag', 'speed'
                                                                                                       'busClock',
                          'labelId', 'owners', 'place', 'benchmark', 'benchmarks', 'public', '_links',
                          'forceCreation', 'icon', 'parent']
    cache_control = 'max-age=1, must-revalidate'
    extra_response_fields = ['@type', 'hid', 'pid']
    datasource = {
        'source': 'devices'
    }


class DeviceSubSettings(DeviceSettings):
    _schema = False
    resource_methods = ['POST']
    item_methods = ['DELETE', 'PATCH']
