import copy

from ereuse_devicehub.resources.event.device.settings import place, EventWithOneDevice, EventSubSettingsOneDevice, \
    parent


class Register(EventWithOneDevice):
    device = {
        'type': ['dict', 'string'],  # POST dict, GET str
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        }
    }
    deviceIsNew = {
        'type': 'boolean',
        'default': False,
        'doc': 'Note that prior may 2017 this value is None for everyone.'
    }
    components = {
        'type': ['list', 'string'],  # POST dict, GET str
        'data_relation': {
            'resource': 'devices',
            'field': '_id',
            'embeddable': True
        }
    }
    parent = copy.copy(parent)
    parent['placeholder_disallowed'] = True
    parent['doc'] = 'Please, discover first its parent before registering a component.'

    force = {
        'type': ['boolean']  # Creates a device even if it does not have pid or hid, doesn't affect components
        # An automatic way of generating pid must be set (ex: PID_AS_AUTOINCREMENT)
    }
    place = place


class RegisterSettings(EventSubSettingsOneDevice):
    _schema = Register
    extra_response_fields = EventSubSettingsOneDevice.extra_response_fields + ['device', 'components', 'deviceIsNew']
    fa = 'fa-plus'
    short_description = 'The creation of a new device in the system.'
