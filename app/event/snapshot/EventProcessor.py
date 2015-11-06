from pprint import pprint

from bson import ObjectId
from eve.methods.post import post_internal

from flask import json

from app.Utils import get_resource_name
from app.exceptions import InnerRequestError
from app.app import app

__author__ = 'Xavier Bustamante Talavera'


class EventProcessor:
    def __init__(self):
        self.events = {}
        self.inserts = []
        self.references = {}  # We cannot use device-dict as references and we cannot rely on _id or hid,
        # So we need another reference: the python's id(). One we insert the device we update the dict with _id

    def add_remove(self, component, old_parent):
        self._add('remove', old_parent, component)

    def add_add(self, component, new_parent):
        self._add('add', new_parent, component)

    def add_insert(self, device):
        self.inserts.append(device)

    def add_register(self, component, parent):
        self._add('register', parent, component)

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
        self._insert() # POST of devices is not an event we are going to save as (We save Register).
        new_events = []
        for event_name, common_reference_dict in self.events.items():
            for reference, unique in common_reference_dict.items():
                device = self.references[reference]
                # new_events.append(self._execute('/devices/' + str(device['_id']) + '/events/' + event_name,
                #                               {'components': [str(x['_id']) for x in
                #                                                unique]}))  # 'device': device['_id']
                new_events.append(self._execute(event_name, {
                    '@type': event_name.title(),
                    'device': device['_id'],
                    'components': [str(x['_id']) for x in unique]
                }))
        return new_events

    def _insert(self) -> list:
        """
        Inserts a new device and updates the device dict with the new _id
        :return:
        """
        new_events = []
        for device_to_insert in self.inserts:
            response = self._execute(get_resource_name(device_to_insert['@type']), device_to_insert)
            device_to_insert['_id'] = ObjectId(response['_id'])
            new_events.append(response)
        return new_events

    # noinspection PyProtectedMember
    @staticmethod
    def _execute(url, payload):
        # response = app.test_client().post(url, data=json.dumps(payload), content_type='application/json')
        response = post_internal(url, payload)
        if response[3] != 201:  # statusCode
            raise InnerRequestError(response._status_code, str(response[0]))
        pprint('Executed POST in ' + url + ' for _id ' + str(response[0]['_id']))
        return response[0]  # Actual data

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
