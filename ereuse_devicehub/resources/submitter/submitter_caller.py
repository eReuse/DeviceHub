from multiprocessing import Process, Queue

from ereuse_devicehub.resources.account.role import Role
from ereuse_devicehub.resources.submitter.submitter import ThreadedSubmitter
from ereuse_devicehub.utils import get_last_exception_info
from eve.methods.post import post_internal
from flask import json
from pymongo.errors import DuplicateKeyError


class SubmitterCaller:
    """
    Prepares a submitter in a long-running daemon process, sending events through 'submit'.
    """
    token = None
    """
        The token of the account submitters use to access DeviceHub. It is shared to avoid
        performing login many times.
    """

    def __init__(self, app: 'DeviceHub', submitter: ThreadedSubmitter):
        """
        :param submitter: The submitter class to invoke when called
        """
        self.submitter = submitter
        self.queue = Queue()
        self.process = None
        self.app = app
        if not self.token:  # Maybe it has been already set by another submitter (class attribute)
            self.token = self.prepare_user(app)
        self.prepare_process()

    def submit(self, event_id: str, database: str, resource_name: str, *args):
        """
        Enqueues the event to be submitted through the submitter, in another thread.
        :param event_id: The id of the event to submit. The event is searched in the database through GET.
        :param database: The database to get the event from.
        :param resource_name: The type of the resource in 'resource_name'format.
        :param args: An optional and extra list of optional args to supply to the submitter.
        """
        self.prepare_process()  # We ensure the process is there, and we start it if it died
        self.queue.put((event_id, database, resource_name) + args)

    def prepare_process(self):
        """
        Ensures that the process is up and ready, or prepares one otherwise.
        """
        if not self.process or not self.process.is_alive():
            # noinspection PyArgumentList
            self.process = Process(target=_process,
                                   args=(self.queue, self.token, self.app, self.submitter),
                                   daemon=True)
            self.process.start()

    @staticmethod
    def prepare_user(app):
        with app.test_request_context():
            account = app.config['SUBMITTER_ACCOUNT']
            account.update({'role': Role.SUPERUSER})
            account['@type'] = 'Account'
            account['databases'] = app.config['DATABASES']
            if app.data.find_one_raw('accounts', {'email': account['email']}) is None:
                try:
                    post_internal('accounts', dict(account),
                                  True)  # If we validate, RolesAuth._set_database changes our db
                except DuplicateKeyError:
                    pass
        response = app.test_client().post('login', data=json.dumps(account), content_type='application/json')
        js = json.loads(response.data.decode())
        return js['token']


def _process(queue: Queue, token: str, app, submitter_class=ThreadedSubmitter):
    """
        A representation of a separate process.
        It's a for_all: It blocks waiting for events to log, and when there is an event, it invokes the submitter.
    :param queue: The queue sent from SubmitterCaller.
    :param token: The token of the DeviceHub user Submitter is going to use to get data.
    :param submitter_class: The Submitter *class* to instantiate and use.
    """
    submitter = submitter_class(app, token)
    while True:
        try:
            submitter.submit(*queue.get(True))  # We block ourselves waiting for something in the queue
        except Exception as e:
            submitter.logger.error(get_last_exception_info())
            raise e
