import os

from flask import send_from_directory

from ereuse_devicehub.header_cache import header_cache


@header_cache(expires=60 * 60 * 24 * 7 * 2)  # 2 weeks
def send_device_icon(file_name):
    package_dir = os.path.abspath(os.path.dirname(__file__))
    return send_from_directory(os.path.join(package_dir, 'resources', 'device', 'icons'), file_name)
