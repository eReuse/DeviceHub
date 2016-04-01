from app.exceptions import StandardError, SchemaError


class HidError(StandardError):
    status_code = 422
    title = 'Cannot compute hid'


class DeviceAlreadyExists(SchemaError):
    status_code = 422

    def __init__(self, field, _id):
        self.field = field
        self.message = self._id = _id


class DeviceNotFound(StandardError):
    status_code = 401


class NoDevicesToProcess(StandardError):
    status_code = 400
