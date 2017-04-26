from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent
from ereuse_devicehub.tests.test_resources.test_group import TestGroupBase


class TestAggregate(TestDeviceEvent, TestGroupBase):
    def _test_discovered_devices(self):
        placeholders_id = []
        full_devices = self.devices_id
        for i in range(0, 10):
            placeholder = self.get_fixture('register', '1-placeholder')
            event = self.post_and_check('{}/{}'.format(self.DEVICE_EVENT, 'register'), placeholder)
            placeholders_id.append(event['device'])
        result, status = self._get(self.db1 + '/aggregations/devices/discovered_devices', self.token)
        self.assert200(status)
