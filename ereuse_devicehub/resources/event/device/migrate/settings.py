from ereuse_devicehub.resources.event.device.settings import EventWithDevices, \
    EventSubSettingsMultipleDevices


class Migrate(EventWithDevices):
    to = {
        'excludes': 'from',
        'or': ['from'],  # Excludes + or = xor
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
    returnedSameAs = {
        'excludes': 'to',
        'type': 'dict',
        'propertyschema': {'type': 'url'},
        'valueschema': {
            'type': 'list',
            'valueschema': {'type', 'url'}
        },
        'readonly': True,
        'writeonly': True,
        'doc': 'A mapping of {deviceUrlInAgent1: sameAsValuesAgent2Sent, ...} representing the sameAs '
               'urls that are sent back to the agent that started the Migrate. Those values need to be sent, '
               'and keeping them helps in future debug sessions.'
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
    unsecured = {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                '_id': {
                    'type': 'string',
                    'data_relation': {
                        'resource': 'devices',
                        'field': '_id',
                        'embeddable': True
                    }
                },
                '@type': {
                    'type': 'string'
                },
                'type': {
                    'type': 'string',
                    'allowed': {'model', 'pid'}
                }
            }
        },
        'default': [],
        'readonly': True
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
    extra_response_fields = EventSubSettingsMultipleDevices.extra_response_fields + ['to', 'from', 'returnedSameAs']
    short_description = 'Changes the DeviceHub that contains (i.e. holds) the device.'
    item_methods = ['GET']  # You cannot delete Migrates
