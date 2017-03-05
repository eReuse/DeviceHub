from collections import defaultdict

from flask import current_app

from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.component.hard_drive.settings import HardDrive
from ereuse_devicehub.resources.device.component.processor.settings import Processor
from ereuse_devicehub.resources.device.component.ram_module.settings import RamModule


def update_materialized_computer(device_id: str, components_id: list, add: bool = True):
    update_query = {}
    inc = defaultdict(int)
    total_types = {RamModule.type_name, HardDrive.type_name}
    for component in ComponentDomain.get({'_id': {'$in': components_id}}):
        _type = component['@type']
        if _type in total_types:
            inc[_type] += component.get('size', 0)
        elif _type == Processor.type_name and 'model' in component:
            update_query['$set' if add else '$unset'] = {'processorModel': component['model']}

    sign = 1 if add else -1  # We will add or subtract values depending if adding or removing components
    update_query['$inc'] = {
        'totalRamSize': sign * inc[RamModule.type_name],
        'totalHardDriveSize': sign * inc[HardDrive.type_name]
    }

    if add:
        component_query = {'$addToSet': {'components': {'$each': components_id}}}
    else:
        component_query = {'$pull': {'components': {'$in': components_id}}}
    update_query.update(component_query)
    current_app.data.driver.db['devices'].update({'_id': device_id}, update_query)
