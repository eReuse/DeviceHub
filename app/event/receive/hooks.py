import datetime

from app.rest import execute_post


def transfer_property(receives: list):
    for receive in receives:
        if receive['automaticallyAllocate']:
            a = execute_post('allocate', {
                '@type': 'Allocate',
                'to': receive['receiver'],
                'devices': receive['devices']
            })
            receive['_created'] = receive['_updated'] = a['_created'] + datetime.timedelta(milliseconds=1)
