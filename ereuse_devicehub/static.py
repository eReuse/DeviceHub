import os

from flask import send_from_directory

from ereuse_devicehub.flask_decorators import cache


@cache(expires=604800)
def send_device_icon(path):
    package_dir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(package_dir, 'resources', 'device', 'icons'), path)
