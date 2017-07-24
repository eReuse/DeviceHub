import pickle
from unittest.mock import MagicMock

from assertpy import assert_that
from ereuse_devicehub.resources.event.device.live.hooks import save_ip
from ereuse_devicehub.tests.test_resources.test_events import TestEventWithPredefinedDevices


class TestDeviceHubLive(TestEventWithPredefinedDevices):
    def setUp(self, settings_file=None, url_converters=None):
        super().setUp(settings_file, url_converters)
        self.app.config['MAXMIND_ACCOUNT'] = {
            'user': 'example',
            'license key': 'example'
        }
        self.client = self.app.geoip.client

    def test_init(self):
        """
        The app initializes correctly.
        """
        # 'Live' event should be registered in domain
        assert_that(self.domain).contains('devices_live')
        assert_that(self.domain).is_type_of(dict)
        assert_that(self.app.on_insert_devices_live.targets).contains(save_ip)

    def test_live(self):
        """
        The app receives a POST Live and it processes it correctly, geocoding the result, creating a Live event and
        setting it to the right device.
        """
        # Let's mock insights of geoip so it doesn't call to Maxmind
        fixture = self.get_fixture('live', 'live_insights', parse_json=False, extension='pickle', mode='rb')
        return_insights = pickle.loads(fixture)
        self.client.insights = MagicMock(return_value=return_insights)
        post = {'device': '1', '@type': 'devices:Live'}
        result = self.post_and_check('{}/live'.format(self.DEVICE_EVENT), post)
        # Let's check the registered event.
        live = self.get_and_check(self.EVENTS, '', result['_id'])
        assert_that(self.get_fixture('live', 'event')).is_subset_of(live)
