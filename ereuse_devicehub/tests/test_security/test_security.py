from ereuse_devicehub.tests import TestStandard


class TestSecurity(TestStandard):
    def setUp(self, settings_file=None, url_converters=None):
        super(TestSecurity, self).setUp(settings_file, url_converters)
        self.devices_id = self.get_fixtures_computers()

    def test_access_public_devices(self):
        public_id = self.devices_id[0]
        private_id = self.devices_id[1]
        public_patch = {
            'public': True
        }
        _, status_code = self.patch(self.DEVICES + '/' + public_id, public_patch)
        self.assert200(status_code)
        # We access to the public with credentials and check that it has 'public' field and equals to True
        public, status_code = self.get(self.DEVICES, '', public_id)
        self.assert200(status_code)
        self.assertIn('public', public)
        self.assertTrue(public['public'])
        public_component, _ = self.get(self.DEVICES, '', public['components'][0])
        self.assertIn('public', public_component)
        self.assertTrue(public_component['public'])
        # We access to the public device without credentials
        _, status_code = self.get(self.DEVICES, '', public_id, False)
        self.assert200(status_code)
        # We access to the private device without credentials
        _, status_code = self.get(self.DEVICES, '', private_id, False)
        self.assert401(status_code)
        # We access to all the devices without credentials
        _, status_code = self.get(self.DEVICES, '', None, False)
        self.assert401(status_code)
        # We access to all the devices with credentials
        _, status_code = self.get(self.DEVICES, '', None, True)
        self.assert200(status_code)
        # We access to another item endpoint without credentials
        private_event = self.get_first(self.DEVICE_EVENT)
        _, status_code = self.get(self.DEVICE_EVENT, '', private_event['_id'], False)
        self.assert401(status_code)
