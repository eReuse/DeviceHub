from app.app import app
from app.device.device import Device
from app.exceptions import StandardError


class Place:
    @staticmethod
    def get(_id, projections):
        return app.data.driver.db['places'].find_one({'_id': _id}, projections)

    @staticmethod
    def update_devices(original: set, updated: set, replaced_place_id: str or None):
        """
        Given the original set of devices of a place, and the updated version, it updates the database to achieve
        the updated set of devices.

        :param original:
        :param updated:
        :param replaced_place_id: The identifier of the replaced place. If updated is empty, this value is not used.
        :return:
        """
        devices_to_remove_id = original - updated
        children_to_remove_id = Device.get_components_in_set(devices_to_remove_id)
        devices_to_remove_id |= children_to_remove_id

        devices_to_add_id = updated - original
        children_to_add_id = Device.get_components_in_set(devices_to_add_id)
        devices_to_add_id |= children_to_add_id

        for device_id in devices_to_remove_id:
            Place.device_unset_place(device_id)
        for device_id in devices_to_add_id:
            Place.device_set_place(device_id, replaced_place_id)

    @staticmethod
    def device_set_place(device_id: str, place_id: str):
        device = app.data.driver.db['devices'].find_one({'_id': device_id}, {'place': True})
        if 'place' in device:
            app.data.driver.db['places'].update_one({'_id': device['place']}, {'$pull': {'devices': device_id}})
        app.data.driver.db['devices'].update_one({'_id': device_id}, {'$set': {'place': place_id}})

    @staticmethod
    def device_unset_place(device_id: str):
        app.data.driver.db['devices'].update_one({'_id': device_id}, {'$unset': {'place': ''}})


class CannotDeleteIfHasEvent(StandardError):
    message = "You cannot delete a place where you performed an event."
