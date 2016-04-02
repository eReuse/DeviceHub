import datetime
import time
from datetime import timedelta
from functools import update_wrapper
from functools import wraps
from wsgiref.handlers import format_date_time

from flask import make_response, request, current_app
from setuptools.compat import basestring


def cache(expires=None, round_to_minute=False):
    """
    Add Flask cache response headers based on expires in seconds.

    If expires is None, caching will be disabled.
    Otherwise, caching headers are set to expire in now + expires seconds
    If round_to_minute is True, then it will always expire at the start of a minute (seconds = 0)

    Example usage:

    @app.route('/map')
    @cache(expires=60)
    def index():
      return render_template('index.html')

    """

    def cache_decorator(view):
        @wraps(view)
        def cache_func(*args, **kwargs):
            now = datetime.datetime.now()

            response = make_response(view(*args, **kwargs))
            response.headers['Last-Modified'] = format_date_time(time.mktime(now.timetuple()))

            if expires is None:
                response.headers[
                    'Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
                response.headers['Expires'] = '-1'
            else:
                expires_time = now + datetime.timedelta(seconds=expires)

                if round_to_minute:
                    expires_time = expires_time.replace(second=0, microsecond=0)

                response.headers['Cache-Control'] = 'public'
                response.headers['Expires'] = format_date_time(time.mktime(expires_time.timetuple()))

            return response

        return cache_func

    return cache_decorator


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator
