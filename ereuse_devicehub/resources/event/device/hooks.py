import copy

import pymongo
from flask import current_app
from pydash import chain
from pydash import concat
from pydash import map_
from pydash import map_values
from pydash import merge
from pydash import uniq

from ereuse_devicehub.exceptions import SchemaError
from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.component.settings import Component
from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.settings import Event, DeviceEvent
from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.group.physical.place.domain import NoPlaceForGivenCoordinates, \
    CoordinatesAndPlaceDoNotMatch
from ereuse_devicehub.resources.group.physical.place.domain import PlaceDomain
from ereuse_devicehub.rest import execute_patch, execute_delete
from ereuse_devicehub.utils import Naming


def get_place(resource_name: str, events: list):
    """

    :param resource_name:
    :param events:
    :return:
    """
    if resource_name in Event.resource_names:
        for event in events:
            if 'geo' in event:
                try:
                    place = PlaceDomain.get_with_coordinates(event['geo']['coordinates'])
                except (KeyError, NoPlaceForGivenCoordinates) as e:
                    # Receive and Locate are forced to have a place for their coordinates
                    if event['@type'] in (DeviceEventDomain.new_type(x) for x in ('Receive', 'Locate')):
                        raise e
                else:
                    if 'place' in event:
                        if event['place']['_id'] != str(place['_id']):  # geo 1 place 1
                            raise CoordinatesAndPlaceDoNotMatch()
                    else:
                        event['place'] = place['_id']  # geo 1 place found in DB


def materialize_components(resource_name: str, events: list):
    """
    Materializes the field 'components' of selected events (not all of them) with the union of all the affected
    components, when the event is performed to computers
    :param resource_name:
    :param events:
    :return:
    """
    if resource_name in Event.resource_names:
        for event in events:
            sub_schema = current_app.config['DOMAIN'][resource_name]['schema']
            schema = sub_schema.get('components', {})
            if schema.get('readonly', False) or schema.get('materialized', False):
                event['components'] = list(ComponentDomain.get_components_in_set(event['devices']))


def materialize_parent(resource_name: str, events: list):
    """
    Materializes the field 'parent', only when this field is set as 'materialized'. This is in case of events affecting
    components (such as TestHardDrive or EraseBasic).
    """
    if resource_name in Event.resource_names:
        for event in events:
            sub_schema = current_app.config['DOMAIN'][resource_name]['schema']
            if sub_schema.get('parent', {}).get('materialized', False):
                event['parent'] = ComponentDomain.get_parent(event['device'])['_id']


def set_place(resource_name: str, events: list):
    """
    Sets the place of the devices. This method must execute after 'get_place' of this module.

    The event performs PATCH o\ hf place, so the effect is like setting the devices to the place.
    :param resource_name:
    :param events:
    :return:
    """
    if resource_name in Event.resource_names:
        for event in events:
            if 'place' in event:
                place = PlaceDomain.get_one(event['place'])
                device = [event['device']] if 'device' in event else []
                devices = uniq(place['children'].get('devices', []) + event.get('devices', []) + device)
                patch = {'@type': 'Place', 'label': place['label'], 'children': {'devices': devices}}
                execute_patch('places', patch, identifier=place['_id'])


def unset_place(resource_name: str, event: dict):
    if resource_name in Event.resource_names:
        if 'place' in event:
            place = PlaceDomain.get_one(event['place'])
            device = [event['device']] if 'device' in event else []
            devices = list(set(place['children'].get('devices', [])) - set(event.get('devices', []) + device))
            patch = {'@type': 'Place', 'label': place['label'], 'children': {'devices': devices}}
            execute_patch('places', patch, event['place'])


def delete_events_in_device(resource_name: str, device: dict):
    """
    Deletes the references of the given device in all the events, and deletes the full event if it references only to
    the device.
    """
    if resource_name in Device.resource_names:
        _id = device['_id']
        qin = {'$in': [_id]}
        query = {'$or': [{'device': _id}, {'devices': qin}, {'components': qin}], '@type': {'$ne': 'devices:Register'}}
        sort = {'_created': pymongo.ASCENDING}  # Order is important to find the first Snapshot (see below)
        first_snapshot_found = False
        for event in DeviceEventDomain.get({'$query': query, '$orderby': sort}):
            if not first_snapshot_found and event['@type'] == 'devices:Snapshot':
                # We cannot delete the Snapshot that created the device, because there is a change to create
                # an infinite loop: Snapshot that created device -> Register -> DEL /device -> Snapshot that created...
                first_snapshot_found = True
            else:
                event_resource = Naming.resource(event['@type'])
                if event.get('device', None) == _id:  # Am I the 'device' of the event?
                    execute_delete(event_resource, event['_id'])
                elif [_id] == event.get('devices', []):  # Is there no more 'devices' in the event, apart from me?
                    execute_delete(event_resource, event['_id'])
                # All events that do not use 'components' for materialization (aka Add/Remove) should be erased
                # if there are no more components
                elif event['@type'] in ('devices:Add', 'devices:Remove') and event['components'] == [_id]:
                    execute_delete(event_resource, event['_id'])
                else:  # Keep the event; just delete my reference
                    DeviceEventDomain.update_raw(event['_id'], {'$pull': {'devices': qin, 'components': qin}})


def remove_from_other_events(resource_name: str, event: dict):
    """Removes the event from other events (Snapshot's 'event' per example)"""
    if resource_name in DeviceEvent.resource_names:
        update = {'$pull': {'events': {'$in': [event['_id']]}}}
        DeviceEventDomain.update_many_raw({}, update)


def validate_only_components_can_have_parents(snapshots: list):
    """Validates that *parent* in a Snapshot is only present when *device* is a component."""
    for snapshot in snapshots:
        if 'parent' in snapshot and snapshot['device']['@type'] not in Component.types:
            # We cannot do this in Validation due to technical difficulties
            raise OnlyComponentsCanHaveParents('device', snapshot['device']['@type'])


class OnlyComponentsCanHaveParents(SchemaError):
    def __init__(self, field=None, resource_type=None):
        message = 'Only components can be inside a device. Remove "parent" or set the device as a component.' \
                  ' Your device is set as {}.'.format(resource_type)
        super().__init__(field, message)


def fill_devices_field_from_groups(resource_name: str, events: list):
    """Gets all the devices from the passed-in groups and adds them to the 'devices' field so they are processed."""

    def get_descendants(labels: list, group_name: str) -> (list, dict):
        """Obtains devices :-)"""
        group_domain = GroupDomain.children_resources[group_name]

        grouped_descendants = group_domain.get_all_descendants(labels)  # descendants per type: devices: [], lots: []
        del grouped_descendants['component']
        devices_id = grouped_descendants.pop('devices')
        devices_id = chain(devices_id).filter(lambda device: device['@type'] not in Component.types).map_('_id').value()
        grouped_descendants = map_values(grouped_descendants, lambda descendants: map_(descendants, 'label'))
        return devices_id, grouped_descendants

    if resource_name in DeviceEvent.resource_names:
        for event in events:
            if 'groups' in event:
                if event['devices']:
                    raise SchemaError('groups', 'You can\'t set groups and devices in the same event.')
                # python-eve does not copy [] so it leaks what we do to default []
                # https://github.com/pyeve/eve/issues/1016
                # todo try removing it after upgrading eve and cerberus
                event['devices'] = []
                event['originalGroups'] = copy.copy(event['groups'])
                for group_name, labels in event['originalGroups'].items():  # So we don't iterate over changing 'groups'
                    # move resources to event concatenating their arrays values
                    devices, groups = get_descendants(labels, group_name)
                    event['devices'].extend(devices)
                    # We need to add `dest or []` because https://github.com/dgilland/pydash/issues/95
                    merge(event['groups'], groups, callback=lambda dest, source: concat(dest or [], source))
