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
