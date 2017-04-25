from ereuse_devicehub.exceptions import SchemaError
from ereuse_devicehub.resources.device.computer.hooks import update_materialized_computer
from ereuse_devicehub.resources.device.domain import DeviceDomain


def remove_components(events: dict):
    """
    Removes the materialized fields *components*, *totalRamSize*, *totalHardDriveSize* and
    *processorModel* of the computer, and the field *parent* of such components.
    """
    for event in events:
        update_materialized_computer(event['device'], event['components'], add=False)


def check_remove(removes: dict):
    for remove in removes:
        device = DeviceDomain.get_one(remove['device'])
        if any(component not in device['components'] for component in remove['components']):
            raise ComponentIsNotInside('components')


class ComponentIsNotInside(SchemaError):
    message = 'The component is not inside the device so it can\'t be removed.'
