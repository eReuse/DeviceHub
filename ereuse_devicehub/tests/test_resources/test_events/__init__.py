from contextlib import suppress
from time import sleep

from ereuse_devicehub.tests import TestStandard


class TestEvent(TestStandard):
    def assertSimilarDevice(self, input_device: dict or str, created_device: dict or str):
        """
        Checks that the createdDevice is the same as the input one, removing computed values as hid... It uses etag.
        :param input_device Input device needs all the float values to have, by default, ".0", or it won't work
        """
        # todo make sure .0 doesn't crush in real program
        parsed_device = self.parse_device(input_device)
        with self.app.app_context():
            from ereuse_devicehub.resources.device.domain import DeviceDomain
            self.assertTrue(DeviceDomain.seem_equal(self.full(self.DEVICES, parsed_device),
                                                    self.full(self.DEVICES, created_device)))

    def assertSimilarDevices(self, input_devices: list, created_devices: list, same_amount_of_devices=False):
        """
        Every created_device device must seem equal (same fields, except computed ones as hid...)
        as one of the input devices.

        There must be one input device per created device.
        :param input_devices:
        :param created_devices:
        :param same_amount_of_devices: bool Force to both lists to have the same amount of devices
        :return:
        """
        if same_amount_of_devices:
            self.assertEqual(len(input_devices), len(created_devices))
        for created_device in created_devices:
            for input_device in input_devices:
                with suppress(AssertionError):
                    self.assertSimilarDevice(input_device, created_device)
                    break
            else:
                self.assertTrue(False)  # Not found


class TestEventWithPredefinedDevices(TestEvent):
    def setUp(self, settings_file=None, url_converters=None):
        super(TestEventWithPredefinedDevices, self).setUp(settings_file, url_converters)
        self.place = self.post_fixture(self.PLACES, self.PLACES, 'place')
        self.devices_id = self.get_fixtures_computers()

    def tearDown(self):
        sleep(2)
        super(TestEventWithPredefinedDevices, self).tearDown()
