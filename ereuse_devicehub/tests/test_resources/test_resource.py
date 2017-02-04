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

    def setUp(self, settings_file=None, url_converters=None):
        """
        Creates a dummy sub-type of device. Note that we need to do it before instantiating the app.
        :param settings_file:
        :param url_converters:
        :return:
        """
        super().setUp(settings_file, url_converters)

    def test_resource(self):
        """
        Creates a resource endpoint extending ResourceSettings and RDFS,
        checking that both processes are done correctly,
        performing requests to the endpoint.
        """
        # We create the resource
        self.app.resources.create_and_add(self.dummy_device_name, prefix=None, parent_schema='Device',
                                          schema_fields=self.dummy_device_class,
                                          parent_resource_settings='DeviceSettings',
                                          resource_setting_fields=self.dummy_device_settings)

        # And regenerate the whole domain schema
        self.app.set_resources_to_domain()
        # Let's validate it
        resource_name = Naming.resource(self.dummy_device_name)
        self.assertIn(resource_name, self.domain)
        settings = self.domain[resource_name]
        assert_that(self.dummy_device_class).is_subset_of(settings['schema'])
        assert_that(self.dummy_device_settings).is_subset_of(settings)
        # Let's check we can perform some actions
        # Let's create a dummy device
        dummy_device = {'serialNumber': '33', 'model': 'model1', 'manufacturer': '234', self.dummy_field: 'dummyField',
                        '@type': self.dummy_device_name}
        register = {'@type': 'Register', 'device': dummy_device}
        self.post_and_check('{}/{}'.format(self.DEVICE_EVENT, 'register'), register)
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
