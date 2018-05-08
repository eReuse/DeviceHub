from ereuse_devicehub.resources.event.device.settings import EventSubSettingsOneDevice, \
    EventWithOneDevice, parent_materialized


class TestHardDrive(EventWithOneDevice):
    """
    We decided to take these specific SMART values because of
    https://www.backblaze.com/blog/hard-drive-smart-stats/.
    """
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
    passedLifetime = {
        'type': 'integer'
    }
    parent = parent_materialized
    reallocatedSectorCount = {
        'type': 'integer'
    }
    powerCycleCount = {
        'type': 'integer'
    }
    reportedUncorrectableErrors = {
        'type': 'integer'
    }
    CommandTimeout = {
        'type': 'integer'
    }
    CurrentPendingSectorCount = {
        'type': 'integer'
    }
    OfflineUncorrectable = {
        'type': 'integer'
    }
    RemainingLifetimePercentage = {
        'type': 'integer'
    }


class TestHardDriveSettings(EventSubSettingsOneDevice):
    _schema = TestHardDrive
    fa = 'fa-flask'
    short_description = 'A test of the health of the hard drive'
    item_methods = ['GET']
