from .projection import project


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
