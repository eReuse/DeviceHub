from multiprocessing import Process, Queue
import json
import logging

from eve.methods.post import post_internal
from pymongo.errors import DuplicateKeyError

from app.account.user import Role
from app.app import app
from app.event.logger.grd_logger import GRDLogger
from flask import current_app, g


class Logger:
    """
    Generic class logger. Carries a long-running thread which contains the different logging mechanisms, and sends
    identifiers of events to the respective loggers.
    """
    queue = Queue()
    thread = None
    token = None

    @classmethod
    def log_event(cls, event_id: str, requested_database: str):
        """
        Logs an event.
        """
        if not cls.thread or not cls.thread.is_alive():
            cls._init()
        cls.queue.put((event_id, requested_database))

    @classmethod
    def _init(cls):
        """
        Prepares stuff, just needs to be executed at the beginning, once.
        """
        account = current_app.config['LOGGER_ACCOUNT']
        account.update({'role': Role.SUPERUSER})
        actual_mongo_prefix = g.mongo_prefix  # todo why can't I use current_app.get_mongo_prefix()?
        del g.mongo_prefix
        result = app.data.driver.db.accounts.find_one({'email': account['email']})
        if result is None:
            try:
                post_internal('accounts', dict(account), True)  # If we validate, RolesAuth._set_database will change our db
            except DuplicateKeyError:
                pass
        g.mongo_prefix = actual_mongo_prefix
        response = app.test_client().post('login', data=json.dumps(account), content_type='application/json')
        js = json.loads(response.data.decode())
        cls.token = js['token']
        cls.thread = Process(target=_loop, args=(cls.queue, cls.token))
        cls.thread.daemon = True
        cls.thread.start()


def _loop(queue: Queue, token: str):
    """
    Technically part of Logger, but outside of it for the system need. This method is in the child thread.

    It's a loop: It blocks waiting for events to log. When there is an event, it invokes the loggers. Starts again.
    :param queue:
    :return:
    """
    logging.basicConfig(filename="logs/GRDLogger.log", level=logging.INFO)  # Another process, another logger
    while True:
        event_id, requested_database = queue.get(True)  # We block ourselves waiting for something in the queue
        if current_app.config.get('GRD', True):
            try:
                GRDLogger(event_id, token, current_app.config.get('GRD_DEBUG', False), requested_database, logging)
            except Exception as e:
                logging.error(str(e))
