from ereuse_devicehub.resources.event.device.settings import place, EventWithOneDevice, EventSubSettingsOneDevice


class Register(EventWithOneDevice):
    device = {
        'type': ['dict', 'string'],  # POST dict, GET str
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
    extra_response_fields = EventSubSettingsOneDevice.extra_response_fields + ['device', 'components']
    fa = 'fa-plus'
    short_description = 'The creation of a new device in the system.'
