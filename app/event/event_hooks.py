from bson import ObjectId
from flask import request
from app import app

__author__ = 'busta'

from .Event import Event


def set_type(resource: str, request):
    """
    We just put @type for any post event. Remember type is the first-letter-capitalized vesion of resource.
    :param resource:
    :param request:
    :return:
    """
    if resource in Event.resource_types():
        request.json['@type'] = resource.title()


def embed(resource, response):
    import json
    if resource in Event.resource_types() or resource == 'events':
        try:
            embedded = json.loads(request.args.get('embedded'))
            if embedded.get('events', 0) == 1:
                for event in response['_items']:
                    if event['@type'] == 'Snapshot':
                        ##todo hacerse con GET o embed components no funciona bien :-(
                        event['events'] = list(app.app.data.driver.db['events'].find(
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
