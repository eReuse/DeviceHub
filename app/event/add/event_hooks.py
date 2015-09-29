from app.app import app

__author__ = 'busta'


def add_components(request, payload):
    """
    After add event has been executed, this function adds the new devices
    to the materialized attribute 'components' of the parent device.
    :param request:
    :param payload:
    :return:
    """
    app.data.driver.db['devices'].update(
        {'_id': request.json['device']},
        {'$addToSet': {'components': request.json['components']}}
    )
