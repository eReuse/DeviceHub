from ereuse_devicehub.resources.event.device.settings import EventWithDevices, \
    EventSubSettingsMultipleDevices, materialized_components


class Sell(EventWithDevices):
    components = materialized_components
    components['materialized'] = True
    invoices = {
        'type': 'list',
        'schema': {
            'type': 'media',
            'accept': 'application/pdf'
        },
        'description': 'Upload PDFs that will be stored securely.'
    }
    to = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'embeddable': True,
            'field': '_id'
        },
        'description': 'The one buying the devices.'
    }
    reserve = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'events',
            'embeddable': True,
            'field': '_id'
        },
        'description': 'The reserve this sell confirms.'
    }


class SellSettings(EventSubSettingsMultipleDevices):
    _schema = Sell
    fa = 'fa-money'
    sink = -5
    short_description = 'A successful selling.'
