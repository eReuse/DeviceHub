from ereuse_devicehub.resources.event.device.settings import EventSubSettingsMultipleDevices, EventWithDevices, \
    materialized_components


class Sell(EventWithDevices):
    components = materialized_components
    components['materialized'] = True
    invoices = {
        'type': 'list',
        'schema': {
            'type': 'media',
            'accept': 'application/pdf'
        },
        'description': 'Upload invoices in PDF. You can select multiple by pressing Ctrl or Cmd.'
                       'You won\'t be able to modify them later and we will save them with the name they have.'
    }
    to = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'accounts',
            'embeddable': True,
            'field': '_id'
        },
        'description': 'The user buying the devices.'
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
