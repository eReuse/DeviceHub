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

# Roles specify what users can do generally.
# Locations alter what users can do. Locations permissions > roles. Admins don't get affected by location perms.

BASIC = 'basic'  # Most basic user. Cannot do anything (except its account). Useful for external people.
AMATEUR = 'amateur'  # Can create devices, however can just see and edit the ones it created. Events are restricted.
EMPLOYEE = 'employee'  # Technicians. Full spectre of operations. Can interact with devices of others.
ADMIN = 'admin'  # worker role + manage other users (except superusers). No location restrictions. Can see analytics.
SUPERUSER = 'superuser'  # admin + they don't appear as public users, and they can manage other superusers.
ROLES = [BASIC, AMATEUR, EMPLOYEE, ADMIN, SUPERUSER]
MANAGERS = [ADMIN, SUPERUSER]