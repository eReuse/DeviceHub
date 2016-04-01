from ereuse_devicehub.exceptions import SchemaError


class AlreadyAllocated(SchemaError):
    message = 'All the devices have already been allocated to this account, so nothing has been done.'
    field = 'to'
    pass