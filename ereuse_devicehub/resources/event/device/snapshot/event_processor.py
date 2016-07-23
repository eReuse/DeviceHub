from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.rest import execute_post
from ereuse_devicehub.utils import Naming


class EventProcessor:
    def __init__(self):
        self.events = {}
        self.references = {}  # We cannot use device-dict as references and we cannot rely on _id or hid,
        # So we need another reference: the python's id(). One we insert the device we update the dict with _id

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
        reference = id(common)
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
                log.append(execute_post(Naming.resource(event_name), {
                    '@type': event_name,
                    'device': device['_id'],
                    'components': [str(x['_id']) for x in unique]
                }))
        return log
