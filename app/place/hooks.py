from bson import ObjectId

from app.utils import difference
from app.app import app
from app.device.device import Device


def set_place_in_devices(items: list):
    for item in items:
        if 'devices' in item:
            for device_id in item['devices']:
                _device_set_place(device_id, item['_id'])


def update_place_in_devices(updated_place: dict, original_place: dict):
    if 'devices' in updated_place:  # PATCH do not need to send us devices. For POST, the default is [].
        original = set(original_place['devices'])
        updated = set(updated_place['devices'])

        devices_to_remove_id = original - updated
        children_to_remove_id = Device.get_components_in_set(devices_to_remove_id)
        devices_to_remove_id |= children_to_remove_id

        devices_to_add_id = updated - original
        children_to_add_id = Device.get_components_in_set(devices_to_add_id)
        devices_to_add_id |= children_to_add_id
        total_devices_in_place = updated - devices_to_remove_id | devices_to_add_id

        for device_id in devices_to_remove_id:
            _device_unset_place(device_id)
        for device_id in devices_to_add_id:
            _device_set_place(device_id, updated_place['_id'])
        app.data.driver.db['devices'].update_one({'_id': updated_place['_id']}, {'$set': {'devices': list(total_devices_in_place)}})


def unset_place_in_devices(item):
    for device_id in item['devices']:
        _device_unset_place(device_id)


def _device_set_place(device_id: str, place_id: str):
    device = app.data.driver.db['devices'].find_one({'_id': device_id}, {'place': True})
    if 'place' in device:
        app.data.driver.db['places'].update_one({'_id': device['place']}, {'$pull': {'devices': device_id}})
    app.data.driver.db['devices'].update_one({'_id': device_id}, {'$set': {'place': place_id}})


def _device_unset_place(device_id: str):
    app.data.driver.db['devices'].update_one({'_id': device_id}, {'$unset': {'place': ''}})
