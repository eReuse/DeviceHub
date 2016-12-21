from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.device.computer.hooks import update_materialized_computer
from ereuse_devicehub.resources.device.computer.settings import Computer
from ereuse_devicehub.resources.device.domain import DeviceDomain


class DatabaseUpdate02:
    """
        Updates the database to the version 0.1 of DeviceHub.

        Execute DatabaseUpdate02(app). This class can be initialized as many times without side effects; it is
        idempotent.
    """

    def __init__(self, app):
        for database in app.config['DATABASES']:
            # We need to have an active request to 'trick' set_database and work with the database we want
            with app.test_request_context('/{}/devices'.format(database)):
                print('Starting update process for database {}'.format(AccountDomain.get_requested_database()))
                app.auth._set_database(True)
                self.materialize_component_info()
                print('Database {} successfully updated.'.format(AccountDomain.get_requested_database()))

    @staticmethod
    def materialize_component_info():
        devices = DeviceDomain.get({'@type': Computer.type_name})
        for device in devices:
            if 'components' in device:
                # Let's reset the ram and hard-drive counter
                for _type in ('totalRamSize', 'totalHardDriveSize'):
                    DeviceDomain.update_one_raw(device['_id'], {'$set': {_type: 0}})
                update_materialized_computer(device['_id'], device['components'], add=True)
