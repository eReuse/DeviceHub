from ereuse_devicehub.resources.device.computer.hooks import update_materialized_computer


def add_components(events: list):
    """
    Updates the materialized fields *components*, *totalRamSize*, *totalHardDriveSize* and
    *processorModel* of the computer.
    """
    for event in events:
        update_materialized_computer(event['device'], event['components'], add=True)


def delete_components(_, add: dict):
    """
    Updates the materialized fields *components*, *totalRamSize*, *totalHardDriveSize* and
    *processorModel* of the computer.
    """
    if add.get('@type') == 'devices:Add':
        update_materialized_computer(add['device'], add['components'], add=False)
