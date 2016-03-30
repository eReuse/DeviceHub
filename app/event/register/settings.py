from app.device.schema import Device
from app.event.settings import place, EventWithOneDevice, EventSubSettingsOneDevice


class Register(EventWithOneDevice):
    device = {
        'type': ['dict', 'string'],  # POST dict, GET str
        'schema': Device,  # anyof causes a bug where resource is not set
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        }
    }
    components = {
        'type': ['list', 'string'],  # POST dict, GET str
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        }
    }
    force = {
        'type': ['boolean']  # Creates a device even if it does not have pid or hid, doesn't affect components
        # An automatic way of generating pid must be set (ex: PID_AS_AUTOINCREMENT)
    }
    place = place


class RegisterSettings(EventSubSettingsOneDevice):
    _schema = Register
    extra_response_fields = ['device', 'components']
