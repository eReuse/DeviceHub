from app.app import app


def remove_components(request, payload):
    """
    After add event has been executed, this function adds the new devices
    to the materialized attribute 'components' of the parent device.
    :param request:
    :param payload:
    :return:
    """
    pass
    app.data.driver.db['devices'].update(
        {'_id': request.json['device']},
        {'$pull': {'components': {'$in': request.json['components']}}}
    )
