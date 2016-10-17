from ereuse_devicehub.exceptions import StandardError, SchemaError
from ereuse_devicehub.resources.domain import ResourceNotFound


class HidError(StandardError):
    status_code = 422
    title = 'Cannot compute hid'


class DeviceAlreadyExists(SchemaError):
    status_code = 422

    def __init__(self, field, _id):
        self.field = field
        self.message = self._id = _id


class DeviceNotFound(ResourceNotFound):
    pass


class NoDevicesToProcess(StandardError):
    status_code = 400
