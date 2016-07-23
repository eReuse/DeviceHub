from flask import current_app

from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.settings import Event
from ereuse_devicehub.resources.place.domain import PlaceDomain, NoPlaceForGivenCoordinates, \
    CoordinatesAndPlaceDoNotMatch
from ereuse_devicehub.rest import execute_patch


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
                execute_patch('places', {'devices': list(set(place['devices'] + event['devices']))}, event['place'])
