from ereuse_devicehub.resources.event.device.settings import EventSubSettingsMultipleDevices, EventWithDevices, \
    materialized_components


class CancelReservation(EventWithDevices):
    components = materialized_components
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
        'description': 'Accounts that have been notified for this cancellation.'
    }
    _for = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'embeddable': True,
            'field': '_id'
        },
        'materialized': True
    }
    reserve = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'events',
            'embeddable': True,
            'field': '_id'
        },
        'description': 'The reserve to cancel.',
        'doc': 'Write only a reservation.',
        'required': True,
        'unique': True  # Only one event can have 'reserve'; or a CancelReservation or a Sell
    }


class CancelReservationSettings(EventSubSettingsMultipleDevices):
    _schema = CancelReservation
    fa = 'fa-times'
    sink = -6
    extra_response_fields = EventSubSettingsMultipleDevices.extra_response_fields + ['notify', 'for']
    short_description = 'Cancels a reservation.'
