from bson import ObjectId

from app.Utils import difference
from app.app import app

"""
def add_children(items: list):
    for item in items:
        if 'parent' in item:
            app.data.driver.db['places'].update(
                {'_id': item['parent']},
                {'$push': {'children': item['_id']}}
            )


def remove_children(item: dict):
    if 'parent' in item:
        app.data.driver.db['places'].update(
            {'_id': item['parent']},
            {'$pull': {'children': item['_id']}}
        )


           response = app.test_client().get('places/' + str(item['_id']), environ_base=request.headers.environ)
            place = json.loads(response.data.decode(app.config['ENCODING']))
            place['children'].append(item['parent'])
            response = app.test_client().patch('places/' + str(item['_id']), payload={'children': place['children']},
                                    environ_base=request.headers.environ)
            pass

"""


def set_place_in_devices(items: list):
    for item in items:
        if 'devices' in item:
            for device_id in item['devices']:
                _device_set_place(device_id, item['_id'])


def update_place_in_devices(updated: dict, original: dict):
    if 'devices' in updated:  # PATCH do not need to send us devices. For POST, the default is [].
        devices_to_remove_id = difference(original['devices'], updated['devices'])
        for device_id in devices_to_remove_id:
            _device_unset_place(device_id)
        devices_to_add_places = difference(updated['devices'], original['devices'])
        for device_id in devices_to_add_places:
            _device_set_place(device_id, updated['_id'])


def unset_place_in_devices(item):
    for device_id in item['devices']:
        _device_unset_place(device_id)


def _device_set_place(device_id: ObjectId, place_id: ObjectId):
    app.data.driver.db['devices'].update_one({'_id': device_id}, {'$set': {'place': place_id}})


def _device_unset_place(device_id: ObjectId):
    app.data.driver.db['devices'].update_one({'_id': device_id}, {'$unset': {'place': ''}})
