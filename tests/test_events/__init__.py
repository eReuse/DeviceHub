from time import sleep

from tests import TestStandard


class TestEvent(TestStandard):
        def setUp(self, settings_file=None, url_converters=None):
            super(TestEvent, self).setUp(settings_file, url_converters)
            self.place = self.post_fixture(self.PLACES, 'place')
            vaio = self.post_fixture(self.SNAPSHOT, 'vaio')
            vostro = self.post_fixture(self.SNAPSHOT, 'vostro')
            xps13 = self.post_fixture(self.SNAPSHOT, 'xps13')
            self.devices_id = [self.get(self.EVENTS, '', event['events'][0])[0]['device'] for event in [vaio, vostro, xps13]]

        def tearDown(self):
            sleep(2)
            super(TestEvent, self).tearDown()
