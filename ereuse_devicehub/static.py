import os

from flask import current_app
from flask import send_from_directory

from ereuse_devicehub.flask_decorators import cache


@cache(expires=604800)
def send_device_icon(path):
    return send_from_directory(os.path.join(current_app.config['BASE_DIR'], 'app', 'device', 'icons'), path)
