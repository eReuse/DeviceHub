from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent


class TestAllocate(TestDeviceEvent):
    def test_create_allocate_with_place(self):
        allocate = self.get_fixture('allocate', 'allocate')
        allocate['to'] = self.get_first('accounts')['_id']
        allocate['devices'] = self.devices_id
        self.post_and_check(self.DEVICE_EVENT + '/allocate', allocate)
