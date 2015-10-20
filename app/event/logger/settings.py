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
            Logger.log_event(str(event['_id']))