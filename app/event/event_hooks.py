from bson import ObjectId
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


#def get_events_for_components(resource: str, request, lookup):
    """
    When retrieving for the events of a device, appends all the events where the device is a component.
    :param request:
    :return:
    """
  ##  if resource == 'events':
        # lookup['$or'] = [{'components': {'$exists': True}}, {'components': {'$exists': False}}]
        #lookup['$or'] = [{'components': {'$exists': False}},
        #                 {'components': {'$in': [ObjectId(request.view_args['device'])]}},
        #                 {'device': ObjectId(request.view_args['device'])}]
        #lookup.update({'components': {'$in': [ObjectId(request.view_args['device'])]}})


        #del request.view_args['device']
 #   pass



