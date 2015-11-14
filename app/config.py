__author__ = 'Xavier'

APP_NAME = "DeviceHub"

ENCODING = "utf-8"  # used just in some scenarios where default Flask doesn't happen (default is utf-8)
# SERVER_NAME = 'my.server'
# _SERVER_NAME = SERVER_NAME
_SERVER_NAME = "https://devicehub.ereue.org"  # Name used not by flask or python-eve but for sending it to other servers (can be false :-D)
GRD_DOMAIN = 'https://sandbox.ereuse.org/'


# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Application settings
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

from app.accounts.login.settings import login
