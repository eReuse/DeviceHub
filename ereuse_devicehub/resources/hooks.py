from datetime import datetime

from ereuse_devicehub.exceptions import RedirectToClient
from ereuse_devicehub.utils import get_header_link
from flask import current_app, json
from requests import Response


def redirect_on_browser(_, request, __):
    """
    Redirects the browsers to the client webApp.
    :param request:
    """
    if request.accept_mimetypes.accept_html:
        raise RedirectToClient()


def set_response_headers_and_cache(resource: str, _, payload: Response):
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


def set_date(name: str, resources: dict):
    """Eve's date is not precise enough (up to seconds) for massive insertion of resources."""
    for resource in resources:
        if name != 'devices_snapshot' and name != 'devices_register':
            # Snapshot and Register will call this method on it's right time, setting name to None
            resource['_created'] = resource['_updated'] = resource.pop('created', datetime.utcnow())
