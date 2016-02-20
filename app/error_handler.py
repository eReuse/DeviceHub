from flask import Response
from flask.json import jsonify

from app.app import app
from app.exceptions import BasicError
from app.flask_decorators import crossdomain
from app.utils import get_header_link


@app.errorhandler(BasicError)
@crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
def handle_standard_error(error: BasicError) -> Response:
    response = jsonify(error.to_dict())
    header_name, header_value = get_header_link(type(error).__name__)
    response.headers[header_name] = header_value
    response.status_code = error.status_code
    return response
