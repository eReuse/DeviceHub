from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.domain import Domain
from ereuse_devicehub.resources.place.settings import PlaceSettings
from flask import current_app


class PlaceDomain(Domain):
    resource_settings = PlaceSettings

    @staticmethod
    def get_with_coordinates(coordinates: list) -> dict:
        """
        Gets a place that intersects the given Point coordinates.
        :param coordinates: GEOJSON coordinates that represent a Point
        :return: place
        """
        place = current_app.data.find_one_raw('places', {
            'geo': {
                '$geoIntersects': {
                    '$geometry': {
                        'type': 'Point',
                        'coordinates': coordinates
                    }
                }
            }
        })
        if not place:
            raise NoPlaceForGivenCoordinates()
        return place

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
        children_to_remove_id = ComponentDomain.get_components_in_set(list(devices_to_remove_id))
        devices_to_remove_id |= children_to_remove_id

        devices_to_add_id = updated - original
        children_to_add_id = ComponentDomain.get_components_in_set(list(devices_to_add_id))
        devices_to_add_id |= children_to_add_id

        for device_id in devices_to_remove_id:
            PlaceDomain.device_unset_place(device_id)
        for device_id in devices_to_add_id:
            PlaceDomain.device_set_place(device_id, replaced_place_id)

    @staticmethod
    def device_set_place(device_id: str, place_id: str):
        device = DeviceDomain.get_one(device_id)
        if 'place' in device:
            current_app.data.driver.db['places'].update_one({'_id': device['place']}, {'$pull': {'devices': device_id}})
        current_app.data.driver.db['devices'].update_one({'_id': device_id}, {'$set': {'place': place_id}})

    @staticmethod
    def device_unset_place(device_id: str):
        current_app.data.driver.db['devices'].update_one({'_id': device_id}, {'$unset': {'place': ''}})


class CannotDeleteIfHasEvent(StandardError):
    message = "You cannot delete a place where you performed an event."


class NoPlaceForGivenCoordinates(StandardError):
    """
    We throw this error if given coordinates do not match any existing place.
    We just throw it in particular cases. Example: Receive and Location.
    """
    status_code = 400
    message = 'There is no place in such coordinates'


class CoordinatesAndPlaceDoNotMatch(StandardError):
    """
    Similar as NoPlaceForGivenCoordinates, this error is thrown when user supplies coordinates
    and a place, and they differ.
    """
    status_code = 400
    message = 'Place and coordinates do not match'
