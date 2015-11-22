from app.app import app
from app.exceptions import CoordinatesAndPlaceDoNotMatch
from app.exceptions import NoPlaceForGivenCoordinates
from .event import Event


def get_place(resource_name: str, events: list):
    if resource_name in Event.resource_types():
        for event in events:
            if 'geo' in event:
                try:
                    place = app.data.driver.db['places'].find_one({
                        'geo': {
                            '$geoIntersects': {
                                '$geometry': {
                                    'type': 'Point',
                                    'coordinates': event['geo']['coordinates']
                                }
                            }
                        }
                    })
                    if not place:
                        raise NoPlaceForGivenCoordinates()
                except (KeyError, NoPlaceForGivenCoordinates) as e:
                    if resource_name == 'receive' or resource_name == 'locate':
                        raise e
                else:
                    if 'place' in event:
                        if event['place']['_id'] != str(place['_id']):  # geo 1 place 1
                            raise CoordinatesAndPlaceDoNotMatch()
                    else:
                        event['place'] = place['_id']  # geo 1 place found in DB
