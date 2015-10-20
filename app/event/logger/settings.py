import json
from logging import getLogger
from bson import ObjectId
from app.app import app
from app.device.Device import Device
from app.device.event_hooks import get_component
from app.event.Event import Event
from app.event.logger.Logger import Logger

__author__ = 'busta'


def get_info_from_hook(resource, events):
    """
    Send info from the hook to the Logger in its thread
    :param resource:
    :param request:
    :param response:
    :return:
    """
    if resource not in ['snapshot'] and resource in [event_type.lower() for event_type in Event.get_types()]:
        for event in events:
            if resource == 'register':  # We need to get them here:  1.we will be out of context, 2. the event should be like this
                e = dict(event)
                e['device'] = Device.get_device_by_id(e['device'])
                e['components'] = [Device.get_device_by_id(component) for component in event['components']]
                Logger.log_event(e)
            else:
                Logger.log_event(event)