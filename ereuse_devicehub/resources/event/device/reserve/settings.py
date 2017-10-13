from ereuse_devicehub.resources.account.settings import unregistered_user_doc, unregistered_user
from ereuse_devicehub.resources.event.device.settings import EventWithDevices, \
    EventSubSettingsMultipleDevices, materialized_components


class Reserve(EventWithDevices):
    components = materialized_components
    deadline = {
        'type': 'datetime'
    }
    _for = {
        'type': ['objectid', 'dict', 'string'],  # We should not add string but it does not work otherwise...
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
        'schema': unregistered_user,
        'get_from_data_relation_or_create': 'email',
        'sink': 2,
        'description': 'Who are you reserving for? If you leave it blank, you will reserve it for yourself.'
        # todo set permissions for only owners setting this field (for now a hook overrides the value)
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
    sell = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'events',
            'embeddable': True,
            'field': '_id'
        },
        'materialized': True,
        'description': 'A Sell event that has completed this reservation.'
    }
    cancel = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'events',
            'embeddable': True,
            'field': '_id'
        },
        'materialized': True,
        'description': 'A CancelReservation event has cancelled this reservation.'
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
