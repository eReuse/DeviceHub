import json
from datetime import datetime

from flask import current_app
from requests import Response
from werkzeug.local import LocalProxy

from ereuse_devicehub.exceptions import RedirectToClient
from ereuse_devicehub.utils import get_header_link

def redirect_on_browser(resource, request, lookup):
    """
    Redirects the browsers to the client webApp.
    :param resource:
    :param request:
    :param lookup:
    :return:
    """
    if request.accept_mimetypes.accept_html:
        raise RedirectToClient()


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


def set_date(_, resources: dict):
    """Eve's date is not precise enough (up to seconds) for massive insertion of resources."""
    for resource in resources:
        resource['_created'] = resource['_updated'] = datetime.utcnow()
