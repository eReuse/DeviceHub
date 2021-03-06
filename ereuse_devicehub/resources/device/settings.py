from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.resource import ResourceSettings

HID_REGEX = '[\w]+-[\w]+-[\w]+'


class DeviceSettings(ResourceSettings):
    resource_methods = ['GET']
    item_methods = ['GET', 'PATCH', 'DELETE']
    _schema = Device
    additional_lookup = {
        'field': 'hid',
        'url': 'regex("' + HID_REGEX + '")'
    }
    item_url = 'regex("[\w]+")'
    etag_ignore_fields = ['hid', '_id', 'components', 'isUidSecured', '_created', '_updated', '_etag', 'speed',
                          'busClock', 'labelId', 'owners', 'place', 'benchmark', 'benchmarks', 'public', '_links',
                          'forceCreation', 'parent', 'events', 'created', 'sameAs', 'placeholder', 'ancestors',
                          'condition', 'perms', '_blacklist']
    cache_control = 'max-age=1, must-revalidate'
    extra_response_fields = ResourceSettings.extra_response_fields + ['hid', 'pid', 'ancestors', 'gid', 'rid', 'perms',
                                                                      'events', 'components']
    datasource = {
        'source': 'devices'
    }
    icon = 'devices/icons/'
    fa = 'fa-desktop'


class DeviceSubSettings(DeviceSettings):
    _schema = False
    resource_methods = ['GET']
    item_methods = ['DELETE', 'GET']
