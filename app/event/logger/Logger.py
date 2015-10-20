from multiprocessing import Process, Queue
from app.event.logger.GRDLogger import GRDLogger

__author__ = 'busta'

class Logger:
    """
    Generic class logger. Carries a long-running thread which contains the different logging mechanisms, and sends
    identifiers of events to the respective loggers.
    """
    queue = Queue()
    thread = None

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
        cls.thread = Process(target=_loop, args=(cls.queue,))
        cls.thread.daemon = True
        cls.thread.start()

def _loop(queue: Queue):
    """
    Technically part of Logger, but outside of it for the system need. This method is in the child thread containing
    the threads.

    It's a loop: It blocks waiting for events to log. When there is an event, it invokes the loggers. Starts again.
    :param queue:
    :return:
    """
    while True:
        event_id = queue.get(True)  # We block ourselves waiting for something in the queue
        GRDLogger(event_id)
