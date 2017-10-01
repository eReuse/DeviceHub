from pprint import pprint
from random import uniform
from unittest.mock import MagicMock

from geojson import Polygon, utils
from passlib.handlers.sha2_crypt import sha256_crypt
from pydash import map_

from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.scripts.create_account import create_account
from ereuse_devicehub.scripts.get_manufacturers import ManufacturersGetter
from ereuse_devicehub.security.perms import ACCESS, READ
from ereuse_devicehub.tests.test_resources.test_events.test_device_event.test_snapshot.test_snapshot import TestSnapshot


class DummyDB:
    """
        Simple class to create a database from 0, adding a dummy user and some devices. Ready to test!

        To use it do the following in your app.py::

            app = DeviceHub()
            d = DummyDB(app)
            d.create_dummy()

        This method uses the test class of TestSnapshot, and the credentials in
        :func:`ereuse_devicehub.tests.TestBase.create_dummy_user`.

    """

    def __init__(self, app):
        self.app = app
        self.test = TestSnapshot()
        self.test.app = self.app
        self.test.prepare()
        self.test.setupDB()
        self.test.create_dummy_user()
        self.test.create_self_machine_account()
        self.computers_id = None

    def create_dummy(self, maximum: int = None):
        """Main dummy function. Creates devices, groups, performs some shares and adds devices to groups."""
        self.create_dummy_devices(maximum)
        computers = self.test.get(self.test.DEVICES, '?where={"@type": "Computer"}')[0]['_items']
        self.computers_id = map_(computers, '_id')
        self.create_dummy_groups()
        self.share_groups()
        ManufacturersGetter().execute(self.app)
        self.create_dummy_lives()
        pprint('Successfully done :-)')

    def create_dummy_devices(self, maximum: int = None):
        self.test.creation = self._creation
        self.test.test_compute_condition_score()
        self.test.test_snapshot_2015_12_09(maximum)
        self.test.post_snapshot(self.test.get_fixture(self.test.SNAPSHOT, 'erase_sectors'))
        self.test.post_snapshot(self.test.get_fixture(self.test.SNAPSHOT, 'erase_sectors_steps'))
        pprint('Finished creating devices.')

    def create_dummy_groups(self):
        for i, computer in enumerate(self.computers_id, start=1):
            package = self.test.get_fixture(self.test.PACKAGES, 'package')
            package['label'] = 'package' + str(i)
            package['children'] = {'devices': [computer]}
            package_id = self.test.post_201(self.test.PACKAGES, package)['_id']
            pallet = self.test.get_fixture(self.test.GROUPS, 'pallet')
            pallet['children'] = {'packages': [package_id]}
            pallet_id = self.test.post_201(self.test.PALLETS, pallet)['_id']
            lot = self.test.get_fixture(self.test.LOTS, 'lot')
            lot['label'] = 'lot' + str(i)
            lot['children'] = {'pallets': [pallet_id]}
            lot_id = self.test.post_201(self.test.LOTS, lot)['_id']
            place = self.test.get_fixture(self.test.PLACES, 'place')
            place['label'] = 'place' + str(i)
            place['geo'] = utils.generate_random(Polygon.__name__)
            # Remember that we need to explicitly add the package to the place
            place['children'] = {'lots': [lot_id], 'packages': [package_id]}
            self.test.post_201(self.test.PLACES, place)
        self.test.post_fixture(self.test.LOTS, self.test.LOTS, 'lot')
        pprint('Finished creating groups')

    def share_groups(self):
        """Shares the first lot to a secondary b@b.b user."""
        self.test.db.accounts.insert_one(
            {
                'email': 'b@b.b',
                'password': sha256_crypt.hash('1234'),
                'role': Role.USER,
                'token': 'TOKENB',
                'databases': {self.app.config['DATABASES'][1]: ACCESS},
                'defaultDatabase': self.app.config['DATABASES'][1],
                '@type': 'Account'
            }
        )
        account2 = self.test.login('b@b.b', '1234')
        lot_patch = {'@type': 'Lot', 'perms': [{'account': account2['_id'], 'perm': READ}]}  # We share the lot
        self.test.patch_200(self.test.LOTS, item=self.test.get_first(self.test.LOTS)['_id'], data=lot_patch)
        pprint('Finished sharing the group')

    def create_dummy_lives(self):
        for computer_id in self.computers_id:
            self.app.geoip.client.insights = MagicMock(return_value=DummyLiveResponse())
            post = {'device': computer_id, '@type': 'devices:Live'}
            self.test.post_201(self.test.DEVICE_EVENT + '/live', post)
        pprint('Finished creating live for computers.')

    def _creation(self, input_snapshot, *args, **kwargs):
        self.test.post_201(self.test.DEVICE_EVENT + '/snapshot', input_snapshot)

    def create_account(self, email: str, password: str, databases: list,
                       role: str = Role.USER, name: str = None, organization: str = None, blocked: bool = False,
                       default_database: str = None, mongo_host: str = None, mongo_port: int = None,
                       db_name: str = 'dh__accounts'):
        print('Creating account {} '.format(email))
        account, hashed_token = create_account(email, password, databases, role, name, organization, blocked,
                                               default_database, mongo_host, mongo_port, db_name)
        print('Account:')
        pprint(account)
        print('Hashed token for REST:')
        print(hashed_token)


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
