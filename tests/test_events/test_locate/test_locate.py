from tests.test_events import TestEvent


class TestLocate(TestEvent):
    def test_create_locate_with_place(self):
        locate = self.get_fixture('locate', 'locate')
        locate['place'] = self.place['_id']
        locate['devices'] = self.devices_id
        self.post_and_check('events/locate', locate)