from flask import current_app

from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.resources.group.physical.domain import PhysicalDomain
from ereuse_devicehub.resources.group.physical.place.settings import PlaceSettings


class PlaceDomain(PhysicalDomain):
    resource_settings = PlaceSettings
    foreign_key_in_device = 'place'



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


class CannotDeleteIfHasEvent(StandardError):
    status_code = 400
    message = 'Delete all the events performed in the place before deleting the place itself.'


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
