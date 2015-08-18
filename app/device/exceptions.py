__author__ = 'busta'

from app.exceptions import StandardError


class HidError(StandardError):
    status_code = 400
    title = 'Cannot compute hid'
