from flask import current_app

from ereuse_devicehub.resources.event.device.settings import Event
from ereuse_devicehub.security.authentication import AccountDomain


def submit_events_to_grd(resource: str, events: list):
    """
    Send info from the hook to the Logger in its thread
    """
    if current_app.config.get('GRD', True) and \
                    resource in current_app.config['EVENTS_IN_GRD'] and resource in Event.resource_types:
        for event in events:
            current_app.grd_submitter_caller.submit(str(event['_id']), AccountDomain.get_requested_database(), resource)
