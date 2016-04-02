from ereuse_devicehub.resources.event.event import Event, EventNotFound
from ereuse_devicehub.resources.place.place import CannotDeleteIfHasEvent, Place


def set_place_in_devices(items: list):
    for item in items:
        if 'devices' in item:
            Place.update_devices(set(), set(item['devices']), item['_id'])


def update_place_in_devices_if_places(updated_place: dict, original_place: dict):
    if 'devices' in updated_place:  # For patch, if no value, it means it is not being updated
        update_place_in_devices(updated_place, original_place)


def update_place_in_devices(replaced_place: dict, original_place: dict):
    Place.update_devices(set(original_place['devices']), set(replaced_place['devices']), replaced_place['_id'])


def unset_place_in_devices(place):
    Place.update_devices(set(place['devices']), set(), None)


def avoid_deleting_if_has_event(item):
    try:
        Event.get_one({'place': item['_id']})
    except EventNotFound:
        pass
    else:
        raise CannotDeleteIfHasEvent()
