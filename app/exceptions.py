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



