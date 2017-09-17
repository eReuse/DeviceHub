import copy

from ereuse_devicehub.resources.event.device.settings import components, EventWithDevices, \
    EventSubSettingsMultipleDevices


class Reserve(EventWithDevices):
    components = copy.deepcopy(components)
    deadline = {
        'type': 'datetime'
    }
    _for = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'embeddable': True,
            'field': '_id'
        },
        'description': 'Who are you reserving for? If you leave it blank, you will reserve it for yourself.'
        # todo set permissions for only owners setting this field
    }
    notify = {
        'type': 'list',
        'schema': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'accounts',
                'embeddable': True,
                'field': '_id'
            }
        },
        'materialized': True,
        'description': 'Accounts that have been notified for this reservation.'
    }

    @classmethod
    def _clean(cls, attributes: dict, attributes_to_remove: tuple = None) -> dict:
        full_dict = super()._clean(attributes, attributes_to_remove)
        full_dict['for'] = full_dict.pop('_for')
        return full_dict


class ReserveSettings(EventSubSettingsMultipleDevices):
    _schema = Reserve
    fa = 'fa-book'
    sink = -5
    extra_response_fields = EventSubSettingsMultipleDevices.extra_response_fields + ['notify', 'for']
    short_description = 'Notifies to the owners of the devices that you (or someone you are on behalf of) ' \
                        'are willing to get or buy the devices.'
