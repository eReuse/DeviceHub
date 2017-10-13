from ereuse_devicehub import DeviceHub
from ereuse_devicehub.resources.account.domain import AccountDomain


class Update:
    """
        Abstract class to update the database.
    """

    def __init__(self, app: DeviceHub, headers=None, update_indexes=False):
        """
        Updates the app.
        :param update_indexes: If true, it will drop all indexes and re-add them from each ResourceSettings.
        """
        self.app = app
        app.config['DEBUG'] = True  # Print log messages on screen
        for database in app.config['DATABASES']:
            # We need to have an active request to 'trick' set_database and work with the database we want
            with app.test_request_context('/{}/devices'.format(database), headers=headers):
                print('Starting update process for database {}'.format(database))
                app.preprocess_request()
                app.auth.set_database_from_url()
                if headers and 'Authorization' in headers:
                    AccountDomain.actual
                self.execute(database)
                if update_indexes:
                    self._update_indexes(update_default_db_ones=False)
                    # Update the indexes of resources that are database-aware
                    print('Updating indexes definition and re-indexing for {}'.format(database))

                print('Database {} successfully updated.'.format(database))
        if update_indexes:
            # We update default dbs
            # for that we create a request context to log in the user
            # but doesn't matter for which database
            with app.test_request_context('/{}/devices'.format(app.config['DATABASES'][0]), headers=headers):
                self._update_indexes(update_default_db_ones=True)

    def execute(self, database):
        """Perform update here. You are in a request context so you can perform any call, like to a Domain class."""
        raise NotImplementedError()

    def _update_indexes(self, update_default_db_ones: bool):
        for domain, indexes in self.app.config['INDEXES']:
            if domain.resource_settings.use_default_database == update_default_db_ones:
                domain.drop_indexes()
                domain.create_indexes(indexes)
