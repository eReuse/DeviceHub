from assertpy import assert_that

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

    def test_type_devices(self):
        URL = '{}/'.format(self.DEVICE_EVENT)
        self.post_and_check(URL + 'ready', {'@type': 'devices:Ready', 'devices': [self.devices_id[0]]})
        self.post_and_check(URL + 'to-repair', {'@type': 'devices:ToRepair', 'devices': [self.devices_id[1]]})
        self.post_and_check(URL + 'dispose', {'@type': 'devices:Dispose', 'devices': [self.devices_id[2]]})
        result, status = self._get(self.db1 + '/aggregations/devices/type')
        self.assert200(status)
        # Note that we are counting components too
        assert_that(result).is_equal_to({'_items': [
            {'@type': 'devices:Dispose', 'count': 10},
            {'@type': 'devices:Snapshot', 'count': 14},
            {'@type': 'devices:ToRepair', 'count': 14},
            {'@type': 'devices:Ready', 'count': 10}
        ]
        })
