import json

from flask import current_app
from requests import Response
from werkzeug.local import LocalProxy

from ereuse_devicehub.exceptions import Redirect
from ereuse_devicehub.utils import get_header_link


# noinspection PyPep8Naming
def set_sameAs(resource_name: str, resources: list):
    """
    Moves the value in the 'url' field to the 'sameAs' field, deleting 'url'.

    When 'url' is set in a POST it means is the URI of another agent, which needs to be converted to our 'sameAs'. In
    another process we will fill 'url' with our URI.
    """
    for resource in resources:
        if 'url' in resource:
            resource['sameAs'] = resource['url']
            del resource['url']


def redirect_on_browser(resource, request, lookup):
    """
    Redirects the browsers to the client webApp.
    :param resource:
    :param request:
    :param lookup:
    :return:
    """
    if request.accept_mimetypes.accept_html:
        raise Redirect()


def set_response_headers_and_cache(resource: str, request: LocalProxy, payload: Response):
    """
    Sets JSON Header link referring to @type
    """
    if (payload._status_code == 200 or payload._status_code == 304) and resource is not None:
        data = json.loads(payload.data.decode(payload.charset))
        resource_type = resource
        try:
            resource_type = data['@type']
        except KeyError:
            if payload._status_code == 304:
                payload.cache_control.max_age = current_app.config['ITEM_CACHE']
        else:
            # If we are here it means it is an item endpoint, not a list (resource) endpoint
            payload.cache_control.max_age = current_app.config['ITEM_CACHE']
        payload.headers._list.append(get_header_link(resource_type))