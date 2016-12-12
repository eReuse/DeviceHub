import copy
from contextlib import suppress

from ereuse_devicehub.exceptions import InnerRequestError
from eve.methods.delete import deleteitem_internal
from eve.methods.patch import patch_internal
from eve.methods.post import post_internal
from flask import request, current_app, json, g


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
    if not (200 <= response._status_code < 300):
        data['url'] = absolute_path_ref
        raise InnerRequestError(response._status_code, data)
    else:
        return data


def execute_get(absolute_path_ref: str, token: bytes = None) -> dict:
    """
    :param absolute_path_ref: The absolute-path reference of the URI;
        `ref <https://tools.ietf.org/html/rfc3986#section-4.2>`_.
    :param token: The *hashed* token.
    """
    http_authorization = request.headers.environ['HTTP_AUTHORIZATION'] if token is None else b'Basic ' + token
    with BlankG():
        response = current_app.test_client().get(absolute_path_ref,
                                                 environ_base={'HTTP_AUTHORIZATION': http_authorization})
    data = json.loads(response.data.decode())  # It is useless to use json_util
    if not (200 <= response._status_code < 300):
        data['url'] = absolute_path_ref
        raise InnerRequestError(response._status_code, data)
    else:
        return data


def execute_patch(resource: str, payload: dict, identifier) -> dict:
    payload['_id'] = str(identifier)
    response = patch_internal(resource, payload, False, False, **{'_id': str(identifier)})
    if not (200 <= response[3] < 300):
        raise InnerRequestError(response[3], response[0])
    return response[0]


def execute_delete(resource: str, identifier):
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
        # todo in flask 0.11 you can use .pop() as a dict
        with suppress(AttributeError):
            self._actual_user = copy.deepcopy(g._actual_user)
            del g._actual_user
        with suppress(AttributeError):
            self.mongo_prefix = copy.deepcopy(g.mongo_prefix)
            del g.mongo_prefix

    def __exit__(self, exc_type, exc_val, exc_tb):
        with suppress(AttributeError):
            g._actual_user = self._actual_user
        with suppress(AttributeError):
            g.mongo_prefix = self.mongo_prefix
