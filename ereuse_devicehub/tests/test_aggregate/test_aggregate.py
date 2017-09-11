from assertpy import assert_that

from ereuse_devicehub.aggregation.aggregation import Aggregation
from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent
from ereuse_devicehub.tests.test_resources.test_group import TestGroupBase


class TestAggregate(TestDeviceEvent, TestGroupBase):
    def setUp(self, settings_file=None, url_converters=None):
        super().setUp(settings_file, url_converters)
        Aggregation.CACHE_TIMEOUT = None

    def _test_discovered_devices(self):
        placeholders_id = []
        full_devices = self.devices_id
        for i in range(0, 10):
            placeholder = self.get_fixture('register', '1-placeholder')
            event = self.post_201('{}/{}'.format(self.DEVICE_EVENT, 'register'), placeholder)
            placeholders_id.append(event['device'])
        self.get_200('aggregations', item='devices/discovered_devices')

    def test_type_devices(self):
        URL = '{}/'.format(self.DEVICE_EVENT)
        self.post_201(URL + 'ready', {'@type': 'devices:Ready', 'devices': [self.devices_id[0]]})
        self.post_201(URL + 'to-repair', {'@type': 'devices:ToRepair', 'devices': [self.devices_id[1]]})
        self.post_201(URL + 'dispose', {'@type': 'devices:Dispose', 'devices': [self.devices_id[2]]})
        result = self.get_200('aggregations', item='devices/types')
        # Note that we are counting components too
        assert_that(result).is_equal_to({'_items': [
            {'@type': 'devices:Dispose', 'count': 10},
            {'@type': 'devices:Snapshot', 'count': 14},
            {'@type': 'devices:ToRepair', 'count': 14},
            {'@type': 'devices:Ready', 'count': 10}
        ]
        })
