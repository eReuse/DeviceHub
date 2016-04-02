from flask import Response, redirect as flask_redirect, request
from flask.json import jsonify

from ereuse_devicehub.exceptions import BasicError, Redirect
from ereuse_devicehub.flask_decorators import crossdomain
from ereuse_devicehub.utils import get_header_link


class ErrorHandlers:
    """
        Handles the way errors interact with the user. For example, how they are shown.
    """

    def __init__(self, app):
        @app.errorhandler(BasicError)
        @crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
        def handle_standard_error(error: BasicError) -> Response:
            """
                Adapts the visualization of an standard error so it complies with the schema, Hydra.
            """
            response = jsonify(error.to_dict())
            header_name, header_value = get_header_link(type(error).__name__)
            response.headers[header_name] = header_value
            response.status_code = error.status_code
            return response

        @app.errorhandler(Redirect)
        @crossdomain(origin='*', headers=['Content-Type', 'Authorization'])
        def redirect(error: Redirect) -> Response:
            """
                For Redirect exceptions, performs a redirection to the client.
            """
            return flask_redirect(app.config['CLIENT'] + request.full_path)
