from time import sleep

from tests.test_events import TestEvent


class TestReceive(TestEvent):
    def test_create_receive_with_place(self):
        receive = self.get_fixture('receive', 'receive')
        receive['receiver'] = self.get_first('accounts')['_id']
        receive['devices'] = self.devices_id
        receive['place'] = self.place['_id']
        self.post_and_check('events/receive', receive)
