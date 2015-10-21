import random
import string
from app.app import app

__author__ = 'busta'


def add_token(documents):
    # Don't use this in production:
    # You should at least make sure that the token is unique.
    for document in documents:
        token = generate_token()
        while app.data.driver.db['accounts'].find_one({'$in': token}) is not None:
            token = generate_token()
        document["token"] = token


def generate_token() -> str:
    return (''.join(random.choice(string.ascii_uppercase)
                    for x in range(10)))
