from eve.methods.post import post_internal

from app.exceptions import StandardError

__author__ = 'Xavier Bustamante Talavera'


class EventProcessor:
    def __init__(self):
        self.events = {}
        self.inserts = []
        self.references = {}  # We cannot use device-dict as references and we cannot rely on _id or hid,
        # So we need another reference: the python's id(). One we insert the device we update the dict with _id

    def add_remove(self, component, old_parent):
        self._add('Remove', old_parent, component)

    def add_add(self, component, new_parent):
        self._add('Add', new_parent, component)

    def add_insert(self, device):
        self.inserts.append(device)

    def add_register(self, component, parent):
        self._add('Register', parent, component)

    def _add(self, event, common, unique):
        uid = id(common)
        self.references[common] = common
        if not self.events[event][uid]:
            self.events[event][uid] = [unique]
        else:
            self.events[event][uid].append(unique)

    def process(self) -> list:
        """
        Executes all events stored.

        First execute the inserts so the stored devices can get the _id and then executes the rest of events.
        :return: A list of the executed events
        """
        new_events = self._insert()
        for event_name, common_reference in self.events.items():
            for unique in self.events[event_name][common_reference]:
                device = self.references[common_reference]
                new_events.append(self._execute(event_name, {'component': unique, 'device': device}))
        return new_events

    def _insert(self) -> list:
        """
        Inserts a new device and updates the device dict with the new _id
        :return:
        """
        new_events = []
        for device_to_insert in self.inserts:
            response = self._execute('device', device_to_insert)
            device_to_insert['_id'] = response['_id']
            new_events.append(response)
        return new_events

    @staticmethod
    def _execute(resource, payload):
            response = post_internal(resource, payload)
            if response.status != 200:
                raise StandardError(response)
            else:
                return response

    @staticmethod
    def check_viability():
        """
        Checks, for all events in self.events if:
        - the user has permission to execute a concrete event.
        - The event itself can be executed without error
        If any of both conditions are not satisfied an exception will be thrown with details.
        :return:
        """
        pass
