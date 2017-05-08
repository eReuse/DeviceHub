import copy
from pathlib import Path

from ereuse_devicehub.exceptions import WrongQueryParam
from ereuse_devicehub.flask_decorators import crossdomain
from ereuse_devicehub.resources.event.device.register.settings import Register
from ereuse_devicehub.rest import execute_post_internal
from ereuse_devicehub.utils import get_json_from_file
from eve.auth import requires_auth
from flask import Response
from flask import request, jsonify

# We use the placeholder fixture
DIRECTORY = str(Path(__file__).parents[4].joinpath('tests', 'fixtures', 'register'))
PLACEHOLDER = get_json_from_file('1-placeholder.json', DIRECTORY)


@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@requires_auth('resource')
def placeholders(db, resource) -> Response:
    """
    Endpoint to create many placeholders in one query. It expects an empty POST with one **parameter**: *quantity*.
    :return: A dict with *devices*, a list of the _ids created.
    """
    try:
        quantity = int(request.args['quantity'])
        if not 0 < quantity <= 100:
            raise TypeError()
    except:
        raise WrongQueryParam('quantity', 'The query parameter is missing or is not a number > 0 and <= 100.')
    REGISTER = Register.resource_name
    ret = {
        'devices': [execute_post_internal(REGISTER, copy.deepcopy(PLACEHOLDER))['device'] for _ in range(quantity)]
    }
    response = jsonify(ret)
    response.status_code = 201
    return response
