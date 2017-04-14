from pprint import pprint

from geojson import Polygon, utils

from ereuse_devicehub.scripts.get_manufacturers import ManufacturersGetter
from ereuse_devicehub.tests.test_resources.test_events.test_device_event.test_snapshot.test_snapshot import TestSnapshot


class DummyDB:
    """
        Simple class to create a database from 0, adding a dummy user and some devices. Ready to test!

        To use it do the following in your app.py::

            app = DeviceHub()
            d = DummyDB(app)
            d.create_dummy_devices()

        This method uses the test class of TestSnapshot, and the credentials in
        :func:`ereuse_devicehub.tests.TestBase.create_dummy_user`.

    """

    def __init__(self, app):
        self.app = app
        self.test = TestSnapshot()
        self.test.app = self.app
        self.test.prepare()
        self.test.create_dummy_user()
        self.test.create_self_machine_account()

    def create_dummy(self, maximum: int = None):
        self.create_dummy_devices(maximum)
        self.create_dummy_groups(maximum)
        ManufacturersGetter().execute(self.app)

    def create_dummy_devices(self, maximum: int = None):
        self.test.creation = self._creation
        self.test.test_snapshot_2015_12_09(maximum)
        self.test.post_snapshot(self.test.get_fixture(self.test.SNAPSHOT, 'erase_sectors'))
        self.test.post_snapshot(self.test.get_fixture(self.test.SNAPSHOT, 'erase_sectors_steps'))

    def create_dummy_groups(self, maximum: int = None):
        computers = self.test.get(self.test.DEVICES, '?where={"@type": "Computer"}')[0]['_items']
        computers_id = [computer['_id'] for computer in computers]
        for i, computer in enumerate(computers_id, start=1):
            package = self.test.get_fixture(self.test.PACKAGES, 'package')
            package['label'] = 'package' + str(i)
            package['children'] = {'devices': [computer]}
            self.test.post_and_check(self.test.PACKAGES, package)
            lot = self.test.get_fixture(self.test.LOTS, 'lot')
            lot['label'] = 'lot' + str(i)
            lot['children'] = {'packages': ['package' + str(i)]}
            self.test.post_and_check(self.test.LOTS, lot)
            place = self.test.get_fixture(self.test.PLACES, 'place')
            place['label'] = 'place' + str(i)
            place['geo'] = utils.generate_random(Polygon.__name__)
            # Remember that we need to explicitly add the package to the place
            place['children'] = {'lots': ['lot' + str(i)], 'packages': ['package' + str(i)]}
            self.test.post_and_check(self.test.PLACES, place)

        self.test.post_fixture(self.test.LOTS, self.test.LOTS, 'lot')
        pprint('Finished basic creation of devices.')

    def _creation(self, input_snapshot, *args, **kwargs):
        self.test.post_and_check(self.test.DEVICE_EVENT + '/snapshot', input_snapshot)
