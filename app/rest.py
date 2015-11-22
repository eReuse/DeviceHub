import json
from pprint import pprint

from eve.methods.post import post_internal
from flask import request

from app.app import app
from app.exceptions import InnerRequestError


def execute_post(resource: str, payload: dict):
    response = post_internal(resource, payload)
    if response[3] != 201:  # statusCode
        raise InnerRequestError(response[3], response[0])
    pprint('Executed POST in ' + resource + ' for _id ' + str(response[0]['_id']))
    return response[0]  # Actual data


def execute_get(url: str):
    response = app.test_client().get(url, environ_base={'HTTP_AUTHORIZATION': request.headers.environ['HTTP_AUTHORIZATION']})
    data = json.loads(response.data.decode())  # It is useless to use json_util
    if response._status_code != 200:
        raise InnerRequestError(response._status_code, data)
    else:
        return data
