from ereuse_devicehub.resources.group.physical.place.domain import NoPlaceForGivenCoordinates
from ereuse_devicehub.tests.test_resources.test_events.test_device_event import TestDeviceEvent


class TestReceive(TestDeviceEvent):
    def test_create_receive_with_place(self):
        receive = self.get_fixture('receive', 'receive')
        receive['receiver'] = self.get_first('accounts')['_id']
        receive['devices'] = self.devices_id
        receive['place'] = self.place['_id']
        self.post_201(self.DEVICE_EVENT + '/receive', receive)

    def test_receive_from_app(self):
        receive = self.get_fixture('receive', 'receive-from-app')
        receive['devices'] = self.devices_id
        response, status = self.post(self.DEVICE_EVENT + '/receive', receive)
        self.assert_error(response, 400, NoPlaceForGivenCoordinates)
