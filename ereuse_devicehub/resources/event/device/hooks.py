import pymongo
from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.settings import Event, DeviceEvent
from ereuse_devicehub.resources.place.domain import PlaceDomain, NoPlaceForGivenCoordinates, \
    CoordinatesAndPlaceDoNotMatch
from ereuse_devicehub.rest import execute_patch, execute_delete
from ereuse_devicehub.utils import Naming
from flask import current_app


def get_place(resource_name: str, events: list):
    """

    :param resource_name:
    :param events:
    :return:
    """
    if resource_name in Event.resource_types:
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
    if resource_name in Event.resource_types:
        for event in events:
            sub_schema = current_app.config['DOMAIN'][resource_name]['schema']
            if 'components' in sub_schema and sub_schema['components'].get('readonly', False):
                event['components'] = list(ComponentDomain.get_components_in_set(event['devices']))


def materialize_parent(resource_name: str, events: list):
    """
    Materializes the field 'parent' of events that only affect components (such as TestHardDrive or EraseBasic)
    :param resource_name:
    :param events:
    :return:
    """
    if resource_name in Event.resource_types:
        for event in events:
            sub_schema = current_app.config['DOMAIN'][resource_name]['schema']
            if 'parent' in sub_schema:
                event['parent'] = ComponentDomain.get_parent(event['device'])['_id']


def set_place(resource_name: str, events: list):
    """
    Sets the place of the devices. This method must execute after 'get_place' of this module.

    The event performs PATCH of place, so the effect is like setting the devices to the place.
    :param resource_name:
    :param events:
    :return:
    """
    if resource_name in Event.resource_types:
        for event in events:
            if 'place' in event:
                place = PlaceDomain.get_one(event['place'])
                device = [event['device']] if 'device' in event else []
                execute_patch('places', {'devices': list(set(place['devices'] + event.get('devices', []) + device))}, event['place'])


def unset_place(resource_name: str, event: dict):
    if resource_name in Event.resource_types:
        if 'place' in event:
            place = PlaceDomain.get_one(event['place'])
            device = [event['device']] if 'device' in event else []
            devices = event.get('devices', []) + device
            execute_patch('places', {'devices': list(set(place['devices']) - set(devices))}, event['place'])


def delete_events_in_device(resource_name: str, device: dict):
    """
    Deletes the references of the given device in all the events, and deletes the full event if it references only to
    the device.
    """
    if resource_name in Device.resource_types:
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
    if resource_name in DeviceEvent.resource_types:
        update = {'$pull': {'events': {'$in': [event['_id']]}}}
        DeviceEventDomain.update_many_raw({}, update)
