from .projection import project
from flask import current_app

def project_item(resource: str, item: dict):
    project(resource, item)


def project_resource(resource: str, response: dict):
    """
    The same as project_item, but for a whole resource (list of items)
    :param resource:
    :param response:
    :return:
    """
    for item in response['_items']:
        project(resource, item)


def authorize_public(resource_name: str, item: dict):
    """
    Check if the item endpoint needs to be public, if there is a need for.

    :param resource_name:
    :param item:
    """
    if current_app.auth.needs_to_be_public():
        if not item.get('public', False):
            current_app.auth.authenticate()


def deny_public(resource_name: str, response: dict):
    """
    Hack to avoid resource endpoints to be publicly exposed
    :param resource_name:
    :param response:
    """
    if current_app.auth.needs_to_be_public():
        current_app.auth.authenticate()
