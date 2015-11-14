import logging

from app.docs import app
app.config.from_object('app.config')

from event_hooks import event_hooks
event_hooks(app)

from app import error_handler  # We register the error_handler

if __name__ == '__main__':
    logging.basicConfig(filename="logs/log.log", level=logging.INFO)
    app.run()
