from eve.methods.delete import deleteitem_internal
from eve.methods.post import post_internal
from app.app import app
from app.event.snapshot.event_processor import EventProcessor
from app.utils import get_resource_name


def set_components(events: dict):
    """
    Sets the new devices to the materialized attribute 'components' of the parent device.
    """
    for event in events:
        app.data.driver.db['devices'].update(
            {'_id': event['device']},
            {'$set': {'components': event['components']}}
        )


def post_devices(events: dict):
    #todo device POST needs a hook able to control hids, pids, model... for now it delegates this to snapshot and devicehub-client
    posted_devices = []
    try:
        for event in events:
            if type(event['device']) is dict:
                posted_devices.append(EventProcessor.execute(get_resource_name(event['device']['@type']), event['device']))
                event['device'] = posted_devices[-1]['_id']
            for component in event['components']:
                posted_devices.append(EventProcessor.execute(get_resource_name(component['@type']), component))
                event['components'][event['components'].index(component)] = posted_devices[-1]['_id']
    except Exception as e:
        for device in posted_devices:
            deleteitem_internal(get_resource_name(device['@type']), device)
        raise e
