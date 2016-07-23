from flask import current_app

from ereuse_devicehub.resources.event.device.logger.logger import Logger
from ereuse_devicehub.resources.event.device.settings import Event
from ereuse_devicehub.security.authentication import User


def get_info_from_hook(resource: str, events: list):
    """
    Send info from the hook to the Logger in its thread
    """
    if resource in current_app.config['EVENTS_IN_GRD'] and resource in Event.resource_types:
        for event in events:
            Logger.log_event(str(event['_id']), User.get_requested_database())
