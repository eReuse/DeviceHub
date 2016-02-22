import json

from eve.auth import requires_auth
from flask import jsonify
from flask import request

from app.aggregation.aggregation import Aggregation
from app.app import app
from app.flask_decorators import crossdomain


@app.route('/<db>/aggregations/<resource>/<method>', methods=['GET'])
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@requires_auth('resource')
def aggregate_view(db, resource, method):
    """
    Performs a login. We make this out of eve, being totally open.
    :return:
    """
    aggregation = Aggregation(resource)
    m = getattr(aggregation, method)(request.args)
    return jsonify(m)

