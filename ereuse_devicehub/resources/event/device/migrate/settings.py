from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.event.device.settings import EventWithDevices, \
    EventSubSettingsMultipleDevices


class Migrate(EventWithDevices):
    to = {
        'excludes': 'from',
        'type': 'dict',
        'schema': {
            'baseUrl': {
                'type': 'url',
                'doc': 'The scheme, domain, any path to reach the DeviceHub.',
                'required': True
            },
            'database': {
                'type': 'string',
                'doc': 'The name of the database as in the URL',
                'required': True
            },
            'url': {
                'type': 'url',
                'readonly': True,
                'doc': 'The URL of the Migrate in the other database.'
            }
        }
    }
    _from = {
        'excludes': 'to',
        'type': 'url',
        'dh_allowed_write_roles': 'superuser',  # todo it should be a 'machine' role
        'doc': 'This value is only filled by other DeviceHub when transmitting the Migrate'
    }
    devices = {  # As in Snapshot, we do not check now if devices are actual Device
        'type': 'list',
        'schema': {
            'type': ['string', 'dict'],
            'data_relation': {
                'resource': 'devices',
                'field': '_id',
                'embeddable': True
            }
        },
        'doc': 'A list of device identifiers. When one DeviceHub sends a Migrate to the other, '
               'devices are full devices with their components.',
        'required': True
    }
    components = {
        'type': 'list',
        'schema': {
            'type': 'string',
            'data_relation': {
                'resource': 'devices',
                'field': '_id',
                'embeddable': True
            }
        },
        'materialized': True,
        'doc': 'The result of the materialized components'
    }

    @classmethod
    def _clean(cls, attributes: dict, attributes_to_remove: tuple = None) -> dict:
        full_dict = super(Migrate, cls)._clean(attributes, attributes_to_remove)
        full_dict['from'] = full_dict.pop('_from')
        return full_dict


class MigrateSettings(EventSubSettingsMultipleDevices):
    _schema = Migrate
    fa = 'fa-share-alt'
    sink = -6
    extra_response_fields = EventSubSettingsMultipleDevices.extra_response_fields + ['to', 'from']
    short_description = 'Changes the DeviceHub that contains (i.e. holds) the device.'
    item_methods = ['GET']  # You cannot delete Migrates
