from time import sleep

from ereuse_devicehub.tests import TestStandard


class TestEvent(TestStandard):
    def setUp(self, settings_file=None, url_converters=None):
        super(TestEvent, self).setUp(settings_file, url_converters)
        self.place = self.post_fixture(self.PLACES, self.PLACES, 'place')
        self.devices_id = self.get_fixtures_computers()

    def tearDown(self):
        sleep(2)
        super(TestEvent, self).tearDown()
