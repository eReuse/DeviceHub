from flask import jsonify, Response
from app.Utils import get_header_link
from app.app import app

__author__ = 'Xavier Bustamante Talavera'


class StandardError(Exception):
    status_code = 500
    message = None

    def __init__(self, message=""):
        if self.message is None:
            self.message = message

    def to_dict(self):
        return {
            '_error': {
                'message': self.message,
                'code': self.status_code,
                '@type': type(self).__name__
            },
            '_status': 'ERR'
        }


"""class ValidationError(StandardError):
    status_code = 400
    message = 'The element has not passed validation'
"""


class InnerRequestError(StandardError):
    """
    Encapsulates errors produced by internal requests (GET, POST...).
    """
    def __init__(self, status_code, message):
        self.status_code = status_code
        super().__init__(message)


class WrongCredentials(StandardError):
    """
    Error when login and user/pass do not match.
    """
    status_code = 401


class UserIsAnonymous(WrongCredentials):
    pass


class NoPlaceForGivenCoordinates(StandardError):
    """
    We throw this error if given coordinates do not match any existing place.
    We just throw it in particular cases. Example: Receive and Location.
    """
    status_code = 400
    message = 'There is no place in such coordinates'


class CoordinatesAndPlaceDoNotMatch(StandardError):
    """
    Similar as NoPlaceForGivenCoordinates, this error is thrown when user supplies coordinates
    and a place, and they differ.
    """
    status_code = 400
    message = 'Place and coordinates do not match'


@app.errorhandler(StandardError)
def handle_standard_error(error: StandardError) -> Response:
    response = jsonify(error.to_dict())
    header_name, header_value = get_header_link(type(error).__name__)
    response.headers[header_name] = header_value
    response.status_code = error.status_code
    return response
