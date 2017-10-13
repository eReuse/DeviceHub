from ereuse_devicehub.resources.account.settings import unregistered_user
from ereuse_devicehub.resources.event.device.settings import EventSubSettingsMultipleDevices, EventWithDevices, \
    materialized_components


class Sell(EventWithDevices):
    components = materialized_components
    components['materialized'] = True
    invoiceNumber = {
        'type': 'string',
        'description': 'The id of your invoice so they can be linked.'
    }
    shippingDate = {
        'type': 'datetime',
        'description': 'When are the devices going to be ready for shipping?'
    }
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
        'type': ['objectid', 'dict', 'string'],  # We should not add string but it does not work otherwise...
        'data_relation': {
            'resource': 'accounts',
            'field': '_id',
            'embeddable': True,
        },
        'schema': unregistered_user,
        'get_from_data_relation_or_create': 'email',
        'sink': 2,
        'description': 'The user buying.'
    }
    reserve = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'events',
            'embeddable': True,
            'field': '_id'
        },
        'unique': True,  # Only one event can have 'reserve'; or a CancelReservation or a Sell
        'description': 'The reserve this sell confirms.'
    }


class SellSettings(EventSubSettingsMultipleDevices):
    _schema = Sell
    fa = 'fa-money'
    sink = -5
    short_description = 'A successful selling.'
