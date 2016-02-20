import os

from flask import send_from_directory

from app.app import app
from app.flask_decorators import cache


@app.route('/devices/icons/<path:path>')
@cache(expires=604800)
def send_device_icon(path):
    return send_from_directory(os.path.join(app.config['BASE_DIR'], 'app', 'device', 'icons'), path)
