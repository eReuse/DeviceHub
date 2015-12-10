import os
from pprint import pprint
from random import choice
import unittest
from app.utils import nested_lookup
from tests import TestStandard


class TestSnapshot(TestStandard):
    DUMMY_DEVICES = (
        '1_1_Register_one_device_with_components.json',
        '1 - 2 - Register second device with components of first.json',
        '1 - 3 - Register 1-1 but removing motherboard moving processor from 1-2 to 1-1.json',
        '1 - 4 - Register 1-1 but removing processor (which ended again in 1-1) and adding graphicCard.json',
        '2 -1 Same as 1 - 1 processor without hid.json'
    )
    REAL_DEVICES = (
        'vostro.json', 'vaio.json', 'xps13.json'
    )
    RESOURCES_PATH = 'test_events/test_snapshot/resources/'

    def assertSimilarDevice(self, inputDevice: dict, createdDevice: dict):
        """
        Checks that the createdDevice is the same as the input one, removing computed values as hid... It uses etag.
        :param inputDevice Input device needs all the float values to have, by default, ".0", or it won't work
        """
        # todo make sure .0 doesn't crush in real program
        from app.device.device import Device
        with self.app.app_context():
            self.assertTrue(Device.seem_equal(inputDevice, createdDevice))

    def assertSimilarDevices(self, input_devices: list, created_devices: list, same_amount_of_devices=False):
        """
        Every created_device device must seem equal (same fields, except computed ones as hid...) as one of the input devices.

        There must be one input device per created device.
        :param input_devices:
        :param created_devices:
        :param same_amount_of_devices: bool Force to both lists to have the same amount of devices
        :return:
        """
        from app.device.device import Device
        if same_amount_of_devices:
            self.assertEqual(len(input_devices), len(created_devices))
        for created_device in created_devices:
            found = False
            i = 0
            while not found and i < len(input_devices):
                with self.app.app_context():
                    found = Device.seem_equal(input_devices[i], created_device)
                i += 1
            self.assertTrue(found)

    def post_snapshot(self, input_snapshot):
        snapshot, status_code = self.post('snapshot', input_snapshot)
        self.assert201(status_code)
        return snapshot

    def post_snapshot_get_full_events(self, input_snapshot, number_of_events_to_assert):
        snapshot = self.post_snapshot(input_snapshot)
        self.assertEqual(len(snapshot['events']), number_of_events_to_assert)
        events = []
        for event_id in snapshot['events']:
            event, status_code = self.get('events', '', event_id)
            self.assert200(status_code)
            events.append(event)
        return events

    def creation(self, input_snapshot: dict, num_of_events: int = 1):
        pprint("1st time snapshot:")
        events = self.post_snapshot_get_full_events(input_snapshot, num_of_events)
        self.assertLen(events, num_of_events)
        register = events[0]
        self.assertType('Register', register)
        self.assertSimilarDevice(input_snapshot['device'], register['device'])
        self.assertSimilarDevices(input_snapshot['components'], register['components'])
        # We do a snapshot again. We should receive a new snapshot without any event on it.
        pprint("2nd time snapshot:")
        snapshot, status_code = self.post('snapshot', input_snapshot)
        self.assert201(status_code)
        self.assertLen(snapshot['events'], num_of_events - 1)

    def add_remove(self, input_snapshot):
        from app.utils import get_resource_name
        component = choice(input_snapshot['components'])
        found = False
        while not found:
            ignore_fields = self.app.config['DOMAIN'][get_resource_name(component['@type'])]['etag_ignore_fields']
            key = choice(list(component.keys()))
            found = key not in ignore_fields
        if type(component[key]) is int or type(component[key]) is float:
            component[key] += 10
        elif type(component[key]) is str:
            import uuid
            component[key] = uuid.uuid4().hex[:6].upper()
        events = self.post_snapshot_get_full_events(input_snapshot, 3)
        a = 2

    def get_num_events(self, snapshot):
        """
        Get the num of events a snapshot is going to produce, by knowing how many tests are in there.

        todo: compute add/Remove and other events, not just tests.
        :param snapshot:
        :return:
        """
        values = nested_lookup('test', snapshot)
        return len(values) + 1  # 1 == register event itself

    def test_snapshot(self):
        self.test_snapshot_register_easy_1()
        self.test_snapshot_real_devices()
        self.test_snapshot_2015_12_09()

    def test_snapshot_register_easy_1(self):
        """
        Easy test with dummy devices that generates HID, etc. Just registering new devices, no add/remove.
        :return:
        """
        self.creation(self.get_json_from_file(self.RESOURCES_PATH + self.DUMMY_DEVICES[0]))

    def test_snapshot_register_easy_2(self):
        """
        Easy test with dummy devices that generates HID, etc. Just registering new devices, no add/remove.
        :return:
        """
        self.creation(self.get_json_from_file(self.RESOURCES_PATH + self.DUMMY_DEVICES[1]))

    def test_snapshot_register_easy_3(self):
        """
        Easy test with dummy devices that generates HID, etc. Just registering new devices, no add/remove.
        :return:
        """
        self.creation(self.get_json_from_file(self.RESOURCES_PATH + self.DUMMY_DEVICES[2]))

    def test_snapshot_register_easy_4(self):
        """
        Easy test with dummy devices that generates HID, etc. Just registering new devices, no add/remove.
        :return:
        """
        self.creation(self.get_json_from_file(self.RESOURCES_PATH + self.DUMMY_DEVICES[3]))

    def test_snapshot_register_vostro(self):
        """
        Same as `test_snapshot_register_easy` however with real devices (fake serials), with all the risks that takes.
        :return:
        """
        self.creation(self.get_json_from_file(self.RESOURCES_PATH + 'vostro.json'), 2)

    def test_snapshot_register_vaio(self):
        """
        Same as `test_snapshot_register_easy` however with real devices (fake serials), with all the risks that takes.
        :return:
        """
        self.creation(self.get_json_from_file(self.RESOURCES_PATH + self.REAL_DEVICES[1]))

    def test_snapshot_register_dellxps(self):
        """
        Same as `test_snapshot_register_easy` however with real devices (fake serials), with all the risks that takes.
        :return:
        """
        self.creation(self.get_json_from_file(self.RESOURCES_PATH + self.REAL_DEVICES[2]))

    def test_snapshot_register_mounted(self):
        """
        Same as `test_snapshot_register_easy` however with real devices (fake serials), with all the risks that takes.
        :return:
        """
        self.creation(self.get_json_from_file(self.RESOURCES_PATH + 'mounted.json'))

    def test_snapshot_real_devices(self):
        # todo the processor of mounted.json and xps13 generates the same hid, as S/N is 'To be filled...'
        for path in self.REAL_DEVICES:
            snapshot = self.get_json_from_file(self.RESOURCES_PATH + path)
            num_events = self.get_num_events(snapshot)
            self.creation(snapshot, num_events)

    def test_snapshot_2015_12_09(self):
        del self.app.config['DOMAIN']['network-adapter']['schema']['serialNumber']['regex']
        this_directory = os.path.dirname(os.path.realpath(__file__))
        file_directory = os.path.join(this_directory, 'resources', '2015-12-09', 'working')
        for filename in os.listdir(file_directory):
            if 'json' in filename:
                pprint(filename)
                snapshot = self.get_json_from_file(filename, file_directory)
                num_events = self.get_num_events(snapshot)
                self.creation(snapshot, num_events)




