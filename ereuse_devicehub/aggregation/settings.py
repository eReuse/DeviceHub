from ereuse_devicehub.aggregation.aggregation import Aggregation, AggregationError
from ereuse_devicehub.flask_decorators import crossdomain, cache
from eve.auth import requires_auth
from flask import jsonify
from flask import request


@cache(Aggregation.CACHE_TIMEOUT)
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
@requires_auth('resource')
def aggregate_view(db, resource, method):
    """
    Performs a login. We make this out of eve, being totally open.
    :return:
    """
    aggregation = Aggregation(resource)
    if method == '_aggregate':
        raise AggregationError("You cannot use _aggregate.")
    try:
        m = getattr(aggregation, method)(request.args)
    except AttributeError as a:
        raise AggregationError(a.args)
    else:
        return jsonify(m)
