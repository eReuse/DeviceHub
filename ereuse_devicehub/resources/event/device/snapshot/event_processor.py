from collections import OrderedDict

from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.rest import execute_post_internal
from ereuse_devicehub.utils import Naming


class EventProcessor:
    """
    Constructs events in different iterations, adding references (like values in 'component') in each iteration, and
    later in time, once they are fully populated, you can POST them.

    EventProcessor accepts *Remove* and *add* events (although easily more can be added), where for example, the
    *components* array is populated in different iterations. *process* finally POSTS the resulted events.

    EventProcessor executes the events in the order they were first created (internally using an OrderedDict).
    """

    def __init__(self):
        self.events = OrderedDict()
        self.references = {}

    def append_remove(self, component, old_parent):
        self._append(DeviceEventDomain.new_type('Remove'), old_parent, component)

    def append_add(self, component, new_parent):
        self._append(DeviceEventDomain.new_type('Add'), new_parent, component)

    def _append(self, event, common, unique):
        """
        Stores an event so it is executed later.

        :param event:
        :param common: Common property of the event (usually 'device' property).
        :param unique: Unique property of the event (usually 'component' one).
        :return:
        """
        reference = id(common)  # We can't use device-dict as references and we can't rely on _id or hid, so we use id()
        self.references[reference] = common
        self.events.setdefault(event, {}).setdefault(reference, []).append(unique)

    def process(self) -> list:
        """
        Executes all events stored.

        First execute the inserts so the stored devices can get the _id and then executes the rest of events.
        :return: A list of the executed events
        """
        log = []  # log done events
        for event_name, common_reference_dict in self.events.items():
            for reference, unique in common_reference_dict.items():
                device = self.references[reference]
                log.append(execute_post_internal(Naming.resource(event_name), {
                    '@type': event_name,
                    'device': device['_id'],
                    'components': [str(x['_id']) for x in unique]
                }))
        return log
