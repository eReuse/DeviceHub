from eve.methods.patch import patch_internal

from app.app import app
from app.device.device import Device
from app.exceptions import CoordinatesAndPlaceDoNotMatch
from app.exceptions import NoPlaceForGivenCoordinates
from app.place.hooks import _device_set_place
from app.place.place import Place
from app.rest import execute_patch
from .event import Event
from flask import current_app


def get_place(resource_name: str, events: list):
    if resource_name in Event.resource_types():
        for event in events:
            if 'geo' in event:
                try:
                    place = app.data.driver.db['places'].find_one({
                        'geo': {
                            '$geoIntersects': {
                                '$geometry': {
                                    'type': 'Point',
                                    'coordinates': event['geo']['coordinates']
                                }
                            }
                        }
                    })
                    if not place:
                        raise NoPlaceForGivenCoordinates()
                except (KeyError, NoPlaceForGivenCoordinates) as e:
                    if resource_name == 'receive' or resource_name == 'locate':
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
    if resource_name in Event.resource_types():
        for event in events:
            sub_schema = current_app.config['DOMAIN'][resource_name]['schema']
            if 'components' in sub_schema and sub_schema['components'].get('readonly', False):
                event['components'] = list(Device.get_components_in_set(event['devices']))


def materialize_parent(resource_name: str, events: list):
    """
    Materializes the field 'parent' of events that only affect components (such as TestHardDrive or EraseBasic)
    :param resource_name:
    :param events:
    :return:
    """
    if resource_name in Event.resource_types():
        for event in events:
            sub_schema = current_app.config['DOMAIN'][resource_name]['schema']
            if 'parent' in sub_schema:
                event['parent'] = Device.get_parent(event['device'])


def set_place(resource_name: str, events: list):
    """
    Sets the place of the devices. This method must execute after 'get_place' of this module.

    The event performs PATCH of place, so the effect is like setting the devices to the place.
    :param resource_name:
    :param events:
    :return:
    """
    if resource_name in Event.resource_types():
        for event in events:
            if 'place' in event:
                place = Place.get(event['place'], {'devices'})
                execute_patch('places', {'devices': place['devices'] + event['devices']}, event['place'])