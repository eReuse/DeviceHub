from app.event.event import Event
from app.event.logger.grd_logger import NONEXISTENT_EVENTS_IN_GRD
from app.event.logger.logger import Logger
from app.security.authentication import User


def get_info_from_hook(resource, events):
    """
    Send info from the hook to the Logger in its thread
    """
    if resource not in NONEXISTENT_EVENTS_IN_GRD and resource in Event.resource_types():
        for event in events:
            Logger.log_event(str(event['_id']), User.get_requested_database())
