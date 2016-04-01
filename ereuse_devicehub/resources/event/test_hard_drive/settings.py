from ereuse_devicehub.resources.event.settings import parent, EventWithOneDevice, EventSubSettingsOneDevice


class TestHardDrive(EventWithOneDevice):
    type = {
        'type': 'string',
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
        'required': True,
        # IF_VALUE_REQUIRE: (False, ('type', 'lifetime', 'firstError')) todo this can just be done when hard-drive is not
        # nested, so we will be able to activate it when, in snapshot, we can abort TestHardDrive event
    }
    parent = parent


class TestHardDriveSettings(EventSubSettingsOneDevice):
    _schema = TestHardDrive
