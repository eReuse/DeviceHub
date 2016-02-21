import json

from eve.auth import requires_auth
from flask import jsonify
from flask import request

from app.aggregation.aggregation import Aggregation
from app.app import app
from app.flask_decorators import crossdomain


@app.route('/<db>/aggregate/<resource>', methods=['GET'])
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@requires_auth('resource')
def aggregate_view(db, resource):
    """
    Performs a login. We make this out of eve, being totally open.
    :return:
    """
    method = request.args['method']
    aggregation = Aggregation(resource)
    m = getattr(aggregation, method)()
    return jsonify(m)

