import copy
from pprint import pprint
from bson import ObjectId
from eve.methods.post import post_internal
from app.utils import get_resource_name
from app.exceptions import InnerRequestError


# noinspection PyBroadException
class EventProcessor:
    def __init__(self):
        self.events = {}
        self.inserts = []
        self.references = {}  # We cannot use device-dict as references and we cannot rely on _id or hid,
        self.register_parent = None
        self.register_components = []
        # So we need another reference: the python's id(). One we insert the device we update the dict with _id

    def add_remove(self, component, old_parent):
        self._add('remove', old_parent, component)

    def add_add(self, component, new_parent):
        self._add('add', new_parent, component)

    def add_register_parent(self, parent):
        self.register_parent = parent

    def add_register_component(self, component):
        self.register_components.append(component)

    def _add(self, event, common, unique):
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
        new_events = []  # log done events
        self._register(new_events)  # The only problems we can face is with registers. todo extend to add/remove
        for event_name, common_reference_dict in self.events.items():
            for reference, unique in common_reference_dict.items():
                device = self.references[reference]
                new_events.append(self.execute(event_name, {
                    '@type': event_name.title(),
                    'device': device['_id'],
                    'components': [str(x['_id']) for x in unique]
                }))
        return new_events

    def _register(self, new_events: list):
        """
        Performs Register, populating new_events with the results. It adds the new _id to the respective devices
        :param new_events: List to append the newly created
        """
        d = copy.deepcopy({'device': self.register_parent, 'components': self.register_components, '@type': 'Register'})
        if self.register_parent:  # If parent exists we use just one Register for all
            new_events.append(self.execute('register', d))
            i = 0
            for component in self.register_components:  # We copy the identifiers to our devices
                component['_id'] = new_events[-1]['components'][i]
                i += 1
            self.register_parent['_id'] = new_events[-1]['device']
        else:
            for component in self.register_components:
                new_events.append(self.execute('register', {'device': component, '@type': 'Register'}))
                component['_id'] = new_events[-1]['device']

    # noinspection PyProtectedMember
    @staticmethod
    def execute(resource: str, payload: dict):
        response = post_internal(resource, payload)
        if response[3] != 201:  # statusCode
            raise InnerRequestError(response[3], str(response[0]))
        pprint('Executed POST in ' + resource + ' for _id ' + str(response[0]['_id']))
        return response[0]  # Actual data
