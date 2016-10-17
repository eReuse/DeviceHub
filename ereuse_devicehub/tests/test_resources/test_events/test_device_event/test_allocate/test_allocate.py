from assertpy import assert_that
from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent


class TestAllocate(TestDeviceEvent):
    def test_create_allocate_with_place(self):
        allocate = self.get_fixture('allocate', 'allocate')
        to = self.get_first('accounts')['_id']
        allocate['to'] = to
        allocate['devices'] = self.devices_id
        allocate = self.post_and_check(self.DEVICE_EVENT + '/allocate', allocate)
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, '', device_id)
            assert_that(device['owners']).contains(to)
        return allocate

    def test_delete_allocate(self):
        allocate = self.test_create_allocate_with_place()
        self.delete_and_check(self.DEVICE_EVENT + '/allocate/' + allocate['_id'])
        _, status = self.get(self.EVENTS, '', allocate['_id'])
        self.assert404(status)
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, '', device_id)
            assert_that(device['owners']).is_empty()

    def test_delete_allocate_deallocate(self):
        # Now let's create again another allocate and let's add a Remove, then let's delete the remove
        allocate = self.test_create_allocate_with_place()
        data = {'@type': 'devices:Deallocate', 'from': allocate['to'], 'devices': self.devices_id}
        deallocate = self.post_and_check(self.DEVICE_EVENT + '/deallocate', data)
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, '', device_id)
            assert_that(device['owners']).is_empty()
        # Now let's remove the deallocate. We need to re-apply the materialization in owners
        self.delete_and_check(self.DEVICE_EVENT + '/deallocate/' + deallocate['_id'])
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, '', device_id)
            assert_that(device['owners']).contains(allocate['to'])

    def test_allocate_delete_complex(self):
        # Let's make the following:
        # Allocate account A, Allocate acc B, Deallocate A, Allocate again A
        allocate_a = self.test_create_allocate_with_place()
        allocate_b = self.get_fixture('allocate', 'allocate')
        allocate_b['devices'] = self.devices_id
        allocate_b['unregisteredTo'] = {'email': 'b@b.com'}
        allocate_b = self.post_and_check(self.DEVICE_EVENT + '/allocate', allocate_b)
        deallocate_a = {'@type': 'devices:Deallocate', 'from': allocate_a['to'], 'devices': self.devices_id}
        deallocate_a = self.post_and_check(self.DEVICE_EVENT + '/deallocate', deallocate_a)
        allocate_a_2 = self.test_create_allocate_with_place()
        # Let's erase the first Allocate A. The result in 'owners' should be A (for the second allocate) and B.
        self.delete_and_check(self.DEVICE_EVENT + '/allocate/' + allocate_a['_id'])
        for device_id in self.devices_id:
            device, _ = self.get(self.DEVICES, '', device_id)
            assert_that(device['owners']).contains(allocate_a_2['to'], allocate_b['to'])

        # We should have deleted the first Allocate A and deallocate B
        _, status = self.get(self.EVENTS, '', allocate_a['_id'])
        self.assert404(status)
        _, status = self.get(self.EVENTS, '', deallocate_a['_id'])
        self.assert404(status)
        _, status = self.get(self.EVENTS, '', allocate_b['_id'])
        self.assert200(status)
        _, status = self.get(self.EVENTS, '', allocate_a_2['_id'])
        self.assert200(status)
