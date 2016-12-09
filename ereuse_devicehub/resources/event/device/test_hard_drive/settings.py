from ereuse_devicehub.resources.event.device.settings import parent, EventWithOneDevice, EventSubSettingsOneDevice


class TestHardDrive(EventWithOneDevice):
    type = {
        'type': 'string',
        # 'allowed': ['Short Offline', 'Extended Offline']
    }
    status = {
        'type': 'string',
        'required': True
    }
    lifetime = {
        'type': 'integer',
    }
    firstError = {
        'type': 'integer',
        'nullable': True
    }
    snapshot = {
        'type': 'objectid',
        'data_relation': {
            'resource': 'events',
            'field': '_id',
            'embeddable': True
        }
    }
    error = {
        'type': 'boolean',
        'required': True
    }
    parent = parent


class TestHardDriveSettings(EventSubSettingsOneDevice):
    _schema = TestHardDrive
    fa = 'fa-flask'
    short_description = 'A test of the health of the hard drive'
    item_methods = ['GET']
