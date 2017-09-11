from flask import current_app

from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.event.device.settings import Event


def submit_events_to_grd(resource: str, events: list):
    """
    Send info from the hook to the Logger in its thread
    """
    if current_app.config.get('GRD', True) and resource in current_app.config['EVENTS_IN_GRD'] \
            and resource in Event.resource_names:
        for event in events:
            current_app.grd_submitter_caller.submit(str(event['_id']), AccountDomain.requested_database, resource)
