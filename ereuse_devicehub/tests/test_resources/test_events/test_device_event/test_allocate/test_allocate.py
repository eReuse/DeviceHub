from assertpy import assert_that

from ereuse_devicehub.resources.hooks import OnlyLastEventCanBeDeleted
from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent


class TestAllocate(TestDeviceEvent):
    ALLOCATE_URL = TestDeviceEvent.DEVICE_EVENT + '/allocate'
    DEALLOCATE_URL = TestDeviceEvent.DEVICE_EVENT + '/deallocate'

    def test_create_allocate_with_place(self):
        allocate = self.get_fixture('allocate', 'allocate')
        to = self.get_first('accounts')['_id']
        allocate['to'] = to
        allocate['devices'] = self.devices_id
        allocate = self.post_201(self.ALLOCATE_URL, allocate)
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, '', device_id)
            assert_that(device['owners']).contains(to)
        return allocate

    def test_delete_allocate(self):
        allocate = self.test_create_allocate_with_place()
        self.delete_and_check(self.ALLOCATE_URL, item=allocate['_id'])
        _, status = self.get(self.EVENTS, item=allocate['_id'])
        self.assert404(status)
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, item=device_id)
            assert_that(device['owners']).is_empty()

    def test_delete_allocate_deallocate(self):
        # Now let's create again another allocate and let's add a Remove, then let's delete the remove
        allocate = self.test_create_allocate_with_place()
        data = {'@type': 'devices:Deallocate', 'from': allocate['to'], 'devices': self.devices_id}
        deallocate = self.post_201(self.DEALLOCATE_URL, data)
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, item=device_id)
            assert_that(device['owners']).is_empty()
        # Now let's remove the deallocate. We need to re-apply the materialization in owners
        self.delete_and_check(self.DEALLOCATE_URL, item=deallocate['_id'])
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, item=device_id)
            assert_that(device['owners']).contains(allocate['to'])

    def test_allocate_delete_complex(self):
        """Performs several Allocate and Deallocate and then deletes them, ensuring previous states are re-obtained."""
        # Let's make the following:
        # Allocate account A, Allocate acc B, Deallocate A, Allocate again A
        allocate_a = self.test_create_allocate_with_place()
        allocate_b = self.get_fixture('allocate', 'allocate')
        allocate_b['devices'] = self.devices_id
        allocate_b['to'] = {'email': 'b@b.com'}
        allocate_b = self.post_201(self.ALLOCATE_URL, allocate_b)
        deallocate_a = {'@type': 'devices:Deallocate', 'from': allocate_a['to'], 'devices': self.devices_id}
        deallocate_a = self.post_201(self.DEALLOCATE_URL, deallocate_a)
        allocate_a_2 = self.test_create_allocate_with_place()
        # We wouldn't be able to delete Allocate A existing Allocate B
        response, status = self.delete(self.ALLOCATE_URL, item=allocate_a['_id'])
        self.assert_error(response, status, OnlyLastEventCanBeDeleted)

        # Let's erase the second Allocate A. The result in 'owners' should be only B.
        self.delete_and_check(self.ALLOCATE_URL, item=allocate_a_2['_id'])
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, item=device_id)
            assert_that(device['owners']).contains(allocate_b['to'])

        # Now let's erase the deallocate A, the result in 'owners' should be A (for the first Allocate) and B.
        self.delete_and_check(self.DEALLOCATE_URL, item=deallocate_a['_id'])
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, item=device_id)
            assert_that(device['owners']).contains(allocate_a['to'], allocate_b['to'])

        # We should have deleted only the second allocate
        self.get_200(self.EVENTS, item=allocate_a['_id'])
        self.get_200(self.EVENTS, item=allocate_b['_id'])
        _, status = self.get(self.EVENTS, item=deallocate_a['_id'])
        self.assert404(status)
        _, status = self.get(self.EVENTS, item=allocate_a_2['_id'])
        self.assert404(status)
