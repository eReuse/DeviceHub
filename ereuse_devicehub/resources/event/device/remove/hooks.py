from ereuse_devicehub.resources.device.computer.hooks import update_materialized_computer


def remove_components(events: dict):
    """
    Removes the materialized fields *components*, *totalRamSize*, *totalHardDriveSize* and
    *processorModel* of the computer.
    """
    for event in events:
        update_materialized_computer(event['device'], event['components'], add=False)
