from tests.test_events import TestEvent


class TestAllocate(TestEvent):
    def test_create_allocate_with_place(self):
        allocate = self.get_fixture('allocate', 'allocate')
        allocate['to'] = self.get_first('accounts')['_id']
        allocate['devices'] = self.devices_id
        self.post_and_check('events/allocate', allocate)
