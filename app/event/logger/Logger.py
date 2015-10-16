from multiprocessing import Process, Queue
from app.event.logger.GRDLogger import GRDLogger

__author__ = 'busta'

class Logger:
    queue = Queue()

    @classmethod
    def init(cls):
        thread = Process(target=cls._loop, args=(cls.queue,))
        thread.daemon = True
        thread.start()

    @classmethod
    def log_event(cls, event):
        cls.queue.put(event)

    @staticmethod
    def _loop(queue: Queue):
        while True:
            event = queue.get(True)  # We block ourselves waiting for something in the queue
            GRDLogger(event)
