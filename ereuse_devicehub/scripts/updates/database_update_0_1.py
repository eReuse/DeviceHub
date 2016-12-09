import pymongo
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.hooks import MaterializeEvents
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.allocate.allocate import materialize_owners
from ereuse_devicehub.utils import Naming


class DatabaseUpdate01:
    """
        Updates the database to the version 0.1 of DeviceHub.

        Execute DatabaseUpdate01(app). This class can be initialized as many times without side effects; it is
        idempotent.
    """

    def __init__(self, app):
        for database in app.config['DATABASES']:
            # We need to have an active request to 'trick' set_database and work with the database we want
            with app.test_request_context('/{}/devices'.format(database)):
                print('Starting update process for database {}'.format(AccountDomain.get_requested_database()))
                app.auth._set_database(True)
                self.set_prefix()
                self.re_materialize_events()
                self.re_materialize_owners()
                print('Database {} successfully updated.'.format(AccountDomain.get_requested_database()))

    @staticmethod
    def set_prefix():
        for event in DeviceEventDomain.get({}):
            try:
                resource_type = DeviceEventDomain.new_type(event['@type'])
            except TypeError:
                pass
            else:
                DeviceEventDomain.update_raw(event['_id'], {'$set': {'@type': resource_type}})
        print('Events prefixed.')

    @staticmethod
    def re_materialize_events():
        DeviceDomain.update_many_raw({}, {'$set': {'events': []}})
        for event in DeviceEventDomain.get({'$query': {}, '$orderby': {'_created': pymongo.ASCENDING}}):
            MaterializeEvents.materialize_events(Naming.resource(event['@type']), [event])
        print('Events re-materialized.')

    @staticmethod
    def re_materialize_owners():
        for device in DeviceDomain.get({'@type': 'Computer'}):
            materialize_owners([device['_id']])
        print('Owners re-materialized in devices.')
