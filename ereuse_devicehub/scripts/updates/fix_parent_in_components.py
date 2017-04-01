from pydash import find

from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.component.settings import Component
from ereuse_devicehub.resources.event.domain import EventDomain
from ereuse_devicehub.scripts.updates.update import Update


class FixParentInComponents(Update):
    """
    Re-computes 'parent' for components.
    """

    def execute(self, database):
        for component in ComponentDomain.get({'@type': {'$in': Component.types}}):
            # As 'events' is ordered, the first Register or Add will be the prevalent one
            event_id = find(component['events'], lambda e: e['@type'] in {'devices:Register', 'devices:Add'})['_id']
            event = EventDomain.get_one(event_id)
            ComponentDomain.update_one_raw(component['_id'], {'$set': {'parent': event['device']}})
