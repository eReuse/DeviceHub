from functools import lru_cache
from os import listdir
from os.path import join

from ereuse_devicehub.header_cache import header_cache
from flask import Blueprint, Response, current_app, jsonify, url_for

desktop_app = Blueprint('DesktopApp', __name__, static_folder='static')


class DesktopApp:
    """Provides dynamic configuration and updates (URLs to installers) for the eReuse.org Desktop App."""
    def __init__(self, app) -> None:
        super().__init__()
        self.app = app
        app.register_blueprint(desktop_app)

    @staticmethod
    def _get_file(file_name: str) -> dict:
        _, version, other = file_name.split('_')
        architecture, _type = other.split('.')
        return {
            'url': url_for('static', filename=join('desktop_app', file_name)),
            'type': _type,
            'architecture': architecture
        }

    @property
    @lru_cache(maxsize=1)
    def config(self) -> dict:
        installer_names = listdir(join(self.app.static_folder, 'desktop_app'))
        _, version, other = installer_names[0].split('_')
        return {
            'version': version,
            'files': list(map(self._get_file, installer_names)),
        }


@desktop_app.route('/desktop-app')
@header_cache(expires=None)
def config() -> Response:
    """Returns a JSON with config and update information for the eReuse.org Desktop App."""
    return jsonify(current_app.desktop_app.config)
