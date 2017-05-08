from pprint import pprint
from random import uniform
from unittest.mock import MagicMock

from ereuse_devicehub.scripts.get_manufacturers import ManufacturersGetter
from ereuse_devicehub.tests.test_resources.test_events.test_device_event.test_snapshot.test_snapshot import TestSnapshot
from geojson import Polygon, utils
from pydash import map_


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
        self.computers_id = None

    def create_dummy(self, maximum: int = None):
        self.create_dummy_devices(maximum)
        computers = self.test.get(self.test.DEVICES, '?where={"@type": "Computer"}')[0]['_items']
        self.computers_id = map_(computers, '_id')
        self.create_dummy_groups()
        ManufacturersGetter().execute(self.app)
        self.create_dummy_lives()

    def create_dummy_devices(self, maximum: int = None):
        self.test.creation = self._creation
        self.test.test_snapshot_2015_12_09(maximum)
        self.test.post_snapshot(self.test.get_fixture(self.test.SNAPSHOT, 'erase_sectors'))
        self.test.post_snapshot(self.test.get_fixture(self.test.SNAPSHOT, 'erase_sectors_steps'))

    def create_dummy_groups(self):
        for i, computer in enumerate(self.computers_id, start=1):
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

    def create_dummy_lives(self):
        for computer_id in self.computers_id:
            self.app.geoip.client.insights = MagicMock(return_value=DummyLiveResponse())
            post = {'device': computer_id, '@type': 'devices:Live'}
            self.test.post_and_check(self.test.DEVICE_EVENT + '/live', post)
        pprint('Finished creating live for computers.')

    def _creation(self, input_snapshot, *args, **kwargs):
        self.test.post_and_check(self.test.DEVICE_EVENT + '/snapshot', input_snapshot)


class DummyLiveResponse:
    MADRID = 40.41, -3.68
    LONDON = 51.3030, 0.0732
    EUROPE_CENTER = 48.6849, 7.4869

    RANGE_CITY = 0.25
    RANGE_SMALL = 0.5
    RANGE_MEDIUM = 1
    RANGE_BIG = 3

    def __init__(self, center_coords=EUROPE_CENTER, range=RANGE_MEDIUM):
        self.location = self.DummyCord(center_coords, range)
        self.raw = {'traits': {}}

    class DummyCord:
        def __init__(self, center_coords, range):
            self.latitude = uniform(center_coords[0] - range, center_coords[0] + range)
            self.longitude = uniform(center_coords[1] - range, center_coords[1] + range)
            self.accuracy_radius = 100
