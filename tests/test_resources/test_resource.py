from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSubSettings
from ereuse_devicehub.resources.resource import Resource
from ereuse_devicehub.utils import Naming
from tests import TestStandard


class TestResource(TestStandard):
    dummy_device_name = 'DummyDevice'
    dummy_field = 'dummyField'
    dummy_device_class = {dummy_field: {'type': 'string'}}
    dummy_device_settings = {dummy_field: 'just to try'}

    def setUp(self, settings_file=None, url_converters=None):
        """
        Creates a dummy sub-type of device. Note that we need to do it before instantiating the app.
        :param settings_file:
        :param url_converters:
        :return:
        """
        self.create_dummy_type_of_device()
        super().setUp(settings_file, url_converters)

    def create_dummy_type_of_device(self):
        Resource.create(self.dummy_device_name, Device, self.dummy_device_class, DeviceSubSettings, self.dummy_device_settings)

    def test_resource(self):
        """
        Creates a resource endpoint extending ResourceSettings and RDFS, checking that both processes are done correctly,
        performing requests to the endpoint.
        """
        # The endpoint is defined in setUp and created as part of the regular workflow in DeviceHub.
        # Let's validate it.
        resource_name = Naming.resource(self.dummy_device_name)
        self.assertIn(resource_name, self.domain)
        settings = self.domain[resource_name]
        self.assertDictContainsSubset(self.dummy_device_class, settings['schema'])
        self.assertDictContainsSubset(self.dummy_device_settings, settings)
        # Let's check we can perform some actions
        # Let's create a dummy device
        dummy_device = {'serialNumber': '33', 'model': 'model1', 'manufacturer': '234', self.dummy_field: 'dummyField', '@type': self.dummy_device_name}
        _, status_code = self.post(self.DEVICES, dummy_device)
        self.assert201(status_code)
        # And now without the necessary new field
        # wrong_dummy_device = dummy_device
        # del wrong_dummy_device[self.dummy_field]
        # _, status_code = self.post(self.DEVICES, wrong_dummy_device)
        # self.assert422(status_code)
        # Let's get a collection of dummy devices
        _, status_code = self.get(self.DEVICES)
        self.assert200(status_code)
        # Let's get the first dummy device
        dummy_device = self.get_first(self.DEVICES)
        dummy_device['@type'] = self.dummy_device_name
        # Let's try posting other devices, so we know our new resource doesn't affect others
        self.get_fixtures_computers()
