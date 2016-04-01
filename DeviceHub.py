import logging

from ereuse_devicehub.docs import app

if __name__ == '__main__':
    if app.config['LOG']:
        logging.basicConfig(filename="logs/log.log", level=logging.INFO)
    app.run()
