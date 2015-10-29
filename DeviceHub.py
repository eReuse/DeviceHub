import logging
from app.app import app

app.config.from_object('app.config')

from event_hooks import event_hooks
event_hooks(app)

from app.accounts.login.settings import login

if __name__ == '__main__':
    logging.basicConfig(filename="logs/log.log", level=logging.INFO)
    app.run()