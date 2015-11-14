from multiprocessing import Process, Queue
import json

from eve.methods.post import post_internal

from app.app import app
from app.event.logger.grd_logger import GRDLogger


class Logger:
    """
    Generic class logger. Carries a long-running thread which contains the different logging mechanisms, and sends
    identifiers of events to the respective loggers.
    """
    queue = Queue()
    thread = None
    token = None

    @classmethod
    def log_event(cls, event_id: str):
        """
        Logs an event.
        """
        if not cls.thread:
            cls._init()
        cls.queue.put(event_id)

    @classmethod
    def _init(cls):
        """
        Prepares stuff, just needs to be executed at the beginning, once.
        """
        account_to_register = {'email': 'logger', 'password': '43fa22kaxlñ0', 'role': 'employee'}
        account_to_login = dict(account_to_register)
        post_internal('accounts', account_to_register, True)  # If user already existed, do nothing.
        response = app.test_client().post('login', data=json.dumps(account_to_login), content_type='application/json')
        js = json.loads(response.data.decode(app.config['ENCODING']))
        cls.token = js['token']
        cls.thread = Process(target=_loop, args=(cls.queue, cls.token))
        cls.thread.daemon = True
        cls.thread.start()


def _loop(queue: Queue, token: str):
    """
    Technically part of Logger, but outside of it for the system need. This method is in the child thread containing
    the threads.

    It's a loop: It blocks waiting for events to log. When there is an event, it invokes the loggers. Starts again.
    :param queue:
    :return:
    """
    while True:
        event_id = queue.get(True)  # We block ourselves waiting for something in the queue
        GRDLogger(event_id, token)
