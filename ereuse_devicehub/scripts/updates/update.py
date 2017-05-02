from ereuse_devicehub.resources.account.domain import AccountDomain


class Update:
    """
        Abstract class to update the database.
    """

    def __init__(self, app, headers=None):
        self.app = app
        for database in app.config['DATABASES']:
            # We need to have an active request to 'trick' set_database and work with the database we want
            with app.test_request_context('/{}/devices'.format(database), headers=headers):
                print('Starting update process for database {}'.format(AccountDomain.get_requested_database()))
                app.auth._set_database(True)
                self.execute(database)
                print('Database {} successfully updated.'.format(AccountDomain.get_requested_database()))

    def execute(self, database):
        """Perform update here. You are in a request context so you can perform any call, like to a Domain class."""
        raise NotImplementedError()
