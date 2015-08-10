__author__ = 'busta'
from app.event.settings import event
from app.device.settings import device

register = dict(event, **{
    'offline': {
        'type': 'boolean'
    },
    'automatic': {
        'type': 'boolean'
    },
    'devicef': {
        'type': 'dict',
  #      'schema': device
    }
})

register_settings = {
    'resource_methods': ['GET', 'POST'],
    'schema': register,
    'datasource': {
        'source': 'events',
        'filter': {'@type': {'$eq': 'register'}}
    }
}
