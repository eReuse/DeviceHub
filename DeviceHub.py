import logging

from app.docs import app

if __name__ == '__main__':
    logging.basicConfig(filename="logs/log.log", level=logging.INFO)
    app.run()
