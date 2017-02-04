import pymongo

from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.resource import ResourceSettings
from ereuse_devicehub.validation.validation import HID_REGEX


class DeviceSettings(ResourceSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.resource_methods = ['GET']
        self.item_methods = ['GET', 'PATCH', 'DELETE']
        self._schema = Device
        self.additional_lookup = {
            'field': 'hid',
            'url': 'regex("' + HID_REGEX + '")'
        }
        self.item_url = 'regex("[\w]+")'
        self.mongo_indexes = {
            '@type': [('@type', pymongo.DESCENDING)],
            '@type and subtype': [('@type', pymongo.DESCENDING), ('type', pymongo.DESCENDING)],
            '@type and _created': [('@type', pymongo.DESCENDING), ('_created', pymongo.DESCENDING)]
        }
        self.etag_ignore_fields = ['hid', '_id', 'components', 'isUidSecured', '_created', '_updated', '_etag', 'speed',
                                   'busClock', 'labelId', 'owners', 'place', 'benchmark', 'benchmarks', 'public',
                                   '_links',
                                   'forceCreation', 'parent', 'events', 'created', 'sameAs']
        self.cache_control = 'max-age=1, must-revalidate'
        self.extra_response_fields = parent.extra_response_fields + ['hid', 'pid']
        self.datasource = {
            'source': 'devices'
        }
        self.icon = 'devices/icons/'


class DeviceSubSettings(DeviceSettings):
    _schema = False
    resource_methods = ['GET']
    item_methods = ['DELETE', 'GET']
