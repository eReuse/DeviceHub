import os

from flask import current_app
from flask.helpers import _PackageBoundObject


def get_static_as_string(self, path: str) -> str:
    """
    Gets a static file located in the path and returns it as a string. Files are supposed to be UTF-8.

    This function prioritizes loading from the current app's static folder and, if it cannot,
    to the blueprint's / app where this method is executed into.

    Note that this function is placed inside :py:class:`flask.helpers._PackageBoundObject`,
    superclass of Flask and Blueprint.

    :param path: The path of the file, relative from the static folder of the app.
    """
    # Original idea from http://flask.pocoo.org/snippets/77/ and based on open_resource()
    #
    try:
        with open(os.path.join(current_app.static_folder, path), 'r') as f:
            return f.read()
    except (TypeError, FileNotFoundError):
        with open(os.path.join(self.static_folder, path), 'r') as f:
            return f.read()


_PackageBoundObject.get_static_as_string = get_static_as_string
