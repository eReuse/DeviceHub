from bson import ObjectId
from flask import request
from app.app import app
from app.exceptions import CoordenatesAndPlaceDoNotMatch
from app.exceptions import NoPlaceForGivenCoordinates

__author__ = 'busta'

from .Event import Event


def embed(resource, response):
    """
    embed events to Snapshot
    :param resource:
    :param response:
    :return:
    """
    import json
    if resource in Event.resource_types() or resource == 'events':
        try:
            embedded = json.loads(request.args.get('embedded'))
            if embedded.get('events', 0) == 1:
                for event in response['_items']:
                    if event['@type'] == 'Snapshot':
                        ##todo hacerse con GET o embed components no funciona bien :-(
                        event['events'] = list(app.data.driver.db['events'].find(
                            {'_id': {'$in': [ObjectId(e) for e in event['events']]}}))
        except TypeError:
            pass


            # def get_events_for_components(resource: str, request, lookup):
        """
    When retrieving for the events of a device, appends all the events where the device is a component.
    :param request:
    :return:
    """
        ##  if resource == 'events':
        # lookup['$or'] = [{'components': {'$exists': True}}, {'components': {'$exists': False}}]
        # lookup['$or'] = [{'components': {'$exists': False}},
        #                 {'components': {'$in': [ObjectId(request.view_args['device'])]}},
        #                 {'device': ObjectId(request.view_args['device'])}]
        # lookup.update({'components': {'$in': [ObjectId(request.view_args['device'])]}})


        # del request.view_args['device']
        #   pass


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
                    if 'place' in event:
                        if event['place']['_id'] != str(place['_id']):  # geo 1 place 1
                            raise CoordenatesAndPlaceDoNotMatch()
                        else:
                            event['place'] = place['_id']  # geo 1 place found in DB
                except KeyError:
                    if (resource_name == 'receive' or resource_name == 'locate') and 'place' not in event:
                        raise NoPlaceForGivenCoordinates()  # geo 1 place not found in DB.
                        # Place is just strictly needed for Receive and locate.
