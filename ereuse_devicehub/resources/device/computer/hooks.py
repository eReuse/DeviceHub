from collections import defaultdict

from flask import current_app
from pydash import is_empty

from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.component.hard_drive.settings import HardDrive
from ereuse_devicehub.resources.device.component.processor.settings import Processor
from ereuse_devicehub.resources.device.component.ram_module.settings import RamModule
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.utils import Naming


def update_materialized_computer(device_or_id: str or dict, components_id: list, add: bool = True):
    """
    Updates the materialized fields *components*, *totalRamSize*, *totalHardDriveSize* and
    *processorModel* of the computer. For those components, the field *parent* is updated accordingly and they inherit
    the parent's group, if any. Components that are removed from their parent do not loose any group –you need
    to do that manually.

    :param device_or_id: The device or the ID of the device. If you pass the device we avoid getting it from the db.
    :param components_id: Only the added/removed components, not the total of components the device has.
    :param add: A flag that, if it is true or unset, materializations are done as if devices were added to the computer,
    and removed otherwise.
    """
    # Materialize fields in parent
    device_id = device_or_id['_id'] if type(device_or_id) is dict else device_or_id
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
    DeviceDomain.update_one_raw(device_id, update_query)

    # Materialize fields in components
    set_materialized_parent_in_components(device_id, components_id, add)

    # Inherit groups
    if add:
        device = device_or_id if type(device_or_id) is dict else DeviceDomain.get_one(device_id)
        inherit_group(device['ancestors'], components_id)


def set_materialized_parent_in_components(parent_id: str, components_id: list, add: bool = True):
    """Sets materialized field *parent* to *parent_id* in the passed-in *components*"""
    op = '$set' if add else '$unset'
    ComponentDomain.update_many_raw({'_id': {'$in': components_id}}, {op: {'parent': parent_id}})


def inherit_group(computer_ancestors_id: list, components_id: list):
    """Copies the place from the parent device to the new components and materializes them in the place"""
    if not is_empty(computer_ancestors_id):
        ComponentDomain.update_raw(components_id, {'$set': {'ancestors': computer_ancestors_id}})
        for parent in computer_ancestors_id:
            query = {'$addToSet': {'children.components': components_id}}
            GroupDomain.children_resources[Naming.resource(parent['@type'])].update_one_raw(parent['label'], query)
