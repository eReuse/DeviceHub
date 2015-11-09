import json
from bson import ObjectId
from flask import request
from app import app

__author__ = 'busta'
"""

def embed_components(resource, response):
   comm  try:
        embedded = json.loads(request.args.get('embedded'))
    except TypeError:
        pass
    else:

        if embedded.get('components', 0) == 1:
comm
    if '_items' in response:
        for item in response['_items']:
            get_component(item)
    else:
        get_component(response)


def get_component(item):
    if 'components' in item:
        item['components'] = list(app.app.data.driver.db['devices'].find(
            {'_id': {'$in': [ObjectId(e) for e in item['components']]}}))


"""