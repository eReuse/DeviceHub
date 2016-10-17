from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent


class TestReceive(TestDeviceEvent):
    def test_create_receive_with_place(self):
        receive = self.get_fixture('receive', 'receive')
        receive['receiver'] = self.get_first('accounts')['_id']
        receive['devices'] = self.devices_id
        receive['place'] = self.place['_id']
        self.post_and_check(self.DEVICE_EVENT + '/receive', receive)
