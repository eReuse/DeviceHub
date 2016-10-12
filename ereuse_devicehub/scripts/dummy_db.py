from pprint import pprint

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
        self.test_snapshot = TestSnapshot()
        self.test_snapshot.app = self.app
        self.test_snapshot.prepare()
        self.test_snapshot.create_dummy_user()

    def create_dummy_devices(self, maximum: int = None):
        self.test_snapshot.creation = self._creation
        self.test_snapshot.test_condition(maximum)
        self.test_snapshot.post_snapshot(self.test_snapshot.get_fixture(self.test_snapshot.SNAPSHOT, 'erase_sectors'))
        self.test_snapshot.post_snapshot(self.test_snapshot.get_fixture(self.test_snapshot.SNAPSHOT,
                                                                        'erase_sectors_steps'))
        pprint('Finished basic creation of devices.')

    def _creation(self, input_snapshot, *args, **kwargs):
        self.test_snapshot.post_and_check(self.test_snapshot.DEVICE_EVENT + '/snapshot', input_snapshot)
