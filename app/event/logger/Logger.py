from multiprocessing import Process, Queue
from app.event.logger.GRDLogger import GRDLogger

__author__ = 'busta'

class Logger:
    queue = Queue()
    thread = None

    @classmethod
    def log_event(cls, event):
        if not cls.thread:
            cls._init()
        cls.queue.put(event)

    @classmethod
    def _init(cls):
        cls.thread = Process(target=_loop, args=(cls.queue,))
        cls.thread.daemon = True
        cls.thread.start()

def _loop(queue: Queue):
    while True:
        event = queue.get(True)  # We block ourselves waiting for something in the queue
        GRDLogger(event)
