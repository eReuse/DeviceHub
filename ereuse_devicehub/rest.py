import copy
from contextlib import suppress
from urllib.parse import urlencode

from eve.methods.delete import deleteitem_internal
from eve.methods.patch import patch_internal
from eve.methods.post import post_internal
from flask import request, current_app, json, g
from pydash import map_values

from ereuse_devicehub.exceptions import InnerRequestError


def execute_post_internal(resource: str, payload: dict, skip_validation=False) -> dict:
    """Executes POST internally using the same Request, so in the same database, etc."""
    response = post_internal(resource, payload, skip_validation)
    if not (200 <= response[3] < 300):
        raise InnerRequestError(response[3], response[0])
    return response[0]  # Actual data


def execute_post(absolute_path_ref: str, payload: dict, headers: list = None, content_type='application/json'):
    """
    Executes post to the same DeviceHub but in a new connection.
    :param absolute_path_ref: The absolute-path reference of the URI;
        `ref <https://tools.ietf.org/html/rfc3986#section-4.2>`_.
    """
    data = json.dumps(payload)
    with BlankG():
        response = current_app.test_client().post(absolute_path_ref, data=data, content_type=content_type,
                                                  headers=headers or [])
    data = json.loads(response.data.decode())
    if not (200 <= response.status_code < 300):
        data['url'] = absolute_path_ref
        raise InnerRequestError(response.status_code, data)
    else:
        return data


def execute_get(absolute_path_ref: str, token: str or bytes = None, params: dict = None) -> dict:
    """
    Executes GET to the same DeviceHub with a new connection.
    :param params: A dict of key (param names) and values that, if they are dicts, will be passed to json
    :param absolute_path_ref: The absolute-path reference of the URI;
        `ref <https://tools.ietf.org/html/rfc3986#section-4.2>`_.
    :param token: The *hashed* token. If None it will be used the token of the actual request.
    """
    if params:
        absolute_path_ref += '?' + urlencode(map_values(params, lambda v: json.dumps(v) if type(v) is dict else v))
    if token is None:
        auth = request.headers.environ['HTTP_AUTHORIZATION']
    else:
        auth = b'Basic ' + (token if type(token) == bytes else bytes(token, 'utf8'))
    with BlankG():
        response = current_app.test_client().get(absolute_path_ref, environ_base={'HTTP_AUTHORIZATION': auth})
    data = json.loads(response.data.decode())  # It is useless to use json_util
    if not (200 <= response._status_code < 300):
        data['url'] = absolute_path_ref
        raise InnerRequestError(response._status_code, data)
    else:
        return data


def execute_patch(resource: str, payload: dict, identifier, copy_id: bool = True) -> dict:
    """Executes PATCH to the same DeviceHub with a new connection."""
    # todo we shouldn't have to copy the id, as eve thinks you are updating the _id
    if copy_id:
        payload['_id'] = str(identifier)
    response = patch_internal(resource, payload, False, False, **{'_id': str(identifier)})
    if not (200 <= response[3] < 300):
        raise InnerRequestError(response[3], response[0])
    return response[0]


def execute_delete(resource: str, identifier):
    """Executes DELETE to the same DeviceHub with a new connection."""
    _, _, _, status = deleteitem_internal(resource, **{'_id': str(identifier)})
    if status != 204:
        raise InnerRequestError(status, {})


class BlankG:
    """
    Each request is an addition to a Flask 'app stack'. When performing internal requests (like test_client)
    things like G are inherited from parent's stack. This means that we leak those global variables to the new
    requests. This intentional and gome in some scenarios, but it interferes with account and the database usage.

    Use this method with a 'with' statement to remove those global variables that should not get passed to a
    new request; in concrete the actual user and the mongo prefix.
    """

    # The with statement: http://preshing.com/20110920/the-python-with-statement-by-example/
    # G gets inherited by child requests (not siblings): http://stackoverflow.com/a/33382823/2710757
    def __enter__(self):
        with suppress(AttributeError):
            self._actual_user = copy.deepcopy(g.pop('_actual_user'))
        with suppress(AttributeError):
            self.mongo_prefix = copy.deepcopy(g.pop('mongo_prefix'))

    def __exit__(self, exc_type, exc_val, exc_tb):
        with suppress(AttributeError):
            g._actual_user = self._actual_user
        with suppress(AttributeError):
            g.mongo_prefix = self.mongo_prefix
