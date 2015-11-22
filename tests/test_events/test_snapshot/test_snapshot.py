from random import choice

from tests import TestStandard


class TestSnapshot(TestStandard):
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

    def creation(self, input_snapshot: dict):
        events = self.post_snapshot_get_full_events(input_snapshot, 1)
        self.assertLen(events, 1)
        register = events[0]
        self.assertType('Register', register)
        self.assertSimilarDevice(input_snapshot['device'], register['device'])
        self.assertSimilarDevices(input_snapshot['components'], register['components'])
        # We do a snapshot again. We should receive a new snapshot without any event on it.
        snapshot, status_code = self.post('snapshot', input_snapshot)
        self.assert201(status_code)
        self.assertLen(snapshot['events'], 0)

    def test_snapshot(self):
        input_snapshot = self.get_json_from_file('test_events/test_snapshot/test_real_device.json')
        self.creation(input_snapshot)
        #self.add_remove(input_snapshot)

