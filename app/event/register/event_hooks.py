from app.app import app


def set_components(request, payload):
    """
    After Register event has been executed, this function sets the devices
    to the materialized attribute 'components' of the parent device.
    :param request:
    :param payload:
    :return:
    """
    app.data.driver.db['devices'].update(
        {'_id': request.json['device']},
        {'$set': {'components': request.json['components']}}
    )
