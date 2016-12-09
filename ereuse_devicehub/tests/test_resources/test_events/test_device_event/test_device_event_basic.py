from assertpy import assert_that

from ereuse_devicehub.tests import TestBase
from ereuse_devicehub.utils import Naming


class TestDeviceEventBasic(TestBase):
    """
        Tests that take care of the creation and configuration of device events.
    """

    def test_creation(self):
        """
        Tests that device events have been created correctly, taking special care of:
        - All events have been created
        - @type and type
        - URL
        - prefix
        """
        events = ('add', 'allocate', 'deallocate', 'dispose', 'free',
                  'locate', 'ready', 'receive', 'register', 'remove', 'repair', 'snapshot', 'test-hard-drive',
                  'to-dispose', 'to-repair', 'to-prepare')  # all subclasses from DeviceEvent in resource type
        events = ['{}{}{}'.format('devices', Naming.RESOURCE_PREFIX, event) for event in events]  # we prefix them
        events += ['accounts', 'devices', 'computer']  # We check some non-prefixed regular resources...
        assert_that(self.domain).contains_key(*events)
        # Type of snapshot should be 'devices:Snapshot'
        snapshot = self.domain['{}{}{}'.format('devices', Naming.RESOURCE_PREFIX, 'snapshot')]
        assert_that(snapshot['schema']['@type']['allowed']) \
            .is_equal_to({'{}{}{}'.format('devices', Naming.TYPE_PREFIX, 'Snapshot')})
        devices = self.domain['devices']
        # And any other type not subclass from DeviceEvent should be without prefix
        assert_that(devices['schema']['@type']['allowed']).contains('Device', 'Computer', 'HardDrive')  # ...and more

        # Checking that the url generated contains 'devices' for DeviceEvent...
        assert_that(snapshot['url']).is_equal_to('events/devices/snapshot')
        # ...but it doesn't add devices to others (it would be then 'devices/devices')
        assert_that(devices['url']).is_equal_to('devices')
