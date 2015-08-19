__author__ = 'busta'

from app.exceptions import StandardError


class HidError(StandardError):
    status_code = 422
    title = 'Cannot compute hid'
