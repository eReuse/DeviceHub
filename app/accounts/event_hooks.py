import random
import string

from app.app import app


def add_token(documents: dict):
    for document in documents:
        token = generate_token()
        while app.data.driver.db['accounts'].find_one({'token': token}) is not None:
            token = generate_token()
        document["token"] = token


def block_users(documents: dict):
    for document in documents:
        document['active'] = False


def generate_token() -> str:
    return (''.join(random.choice(string.ascii_uppercase)
                    for x in range(10)))
