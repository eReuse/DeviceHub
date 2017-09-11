from assertpy import assert_that

from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSubSettings
from ereuse_devicehub.resources.resource import Resource
from ereuse_devicehub.tests import TestStandard
from ereuse_devicehub.utils import Naming


class TestResource(TestStandard):
    dummy_device_name = 'DummyDevice'
    dummy_field = 'dummyField'
    dummy_device_class = {dummy_field: {'type': 'string'}}
    dummy_device_settings = {dummy_field: 'just to try'}

    def prepare(self):
        DummyDevice, DummyDeviceSettings = Resource.create(self.dummy_device_name, Device, self.dummy_device_class,
                                                           DeviceSubSettings, self.dummy_device_settings)
        self.DummyDevice = DummyDevice
        self.DummyDeviceSettings = DummyDeviceSettings
        # If this test is not called as the first method it is not automatically added to DeviceHub
        # And we need to register the resource directly by executing the following method manually:
        # Note that this method is not needed if Resource.create is called before app = DeviceHub()
        # and that we can't add id in setUp() before calling app = DeviceHub() as python is reusing stuff from memory
        # between tests causing this to fail (can know why?)
        self.app.register_resource(DummyDeviceSettings.resource_name(), DummyDeviceSettings)
        super().prepare()

    def test_resource(self):
        """
        Creates a resource endpoint extending ResourceSettings and RDFS,
        checking that both processes are done correctly,
        performing requests to the endpoint.
        """
        # The endpoint is defined in setUp and created as part of the regular workflow in DeviceHub.
        # Let's validate it.
        resource_name = Naming.resource(self.dummy_device_name)
        assert_that(self.domain).contains(resource_name)
        settings = self.domain[resource_name]
        assert_that(self.dummy_device_class).is_subset_of(settings['schema'])
        assert_that(self.dummy_device_settings).is_subset_of(settings)
        # Let's check we can perform some actions
        # Let's create a dummy device
        dummy_device = {'serialNumber': '33', 'model': 'model1', 'manufacturer': '234', self.dummy_field: 'dummyField',
                        '@type': self.dummy_device_name}
        register = {'@type': 'Register', 'device': dummy_device}
        self.post_201('{}/{}'.format(self.DEVICE_EVENT, 'register'), register)
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
