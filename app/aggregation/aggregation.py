import calendar
import datetime

from flask import current_app
from pymongo import DESCENDING


class Aggregation:
    def __init__(self, resouce_name):
        self.resource_name = resouce_name

    def number_devices_events(self, options):
        pipeline = [
            {
                '$match': {
                    '@type': options['event'],
                    '_created': {'$gte': datetime.datetime(datetime.date.today().year, 1, 1)}
                }
            },
            {
                '$unwind': '$devices'
            },
            {
                '$group': {
                    '_id': {
                        'month': {'$month': '$_created'},
                        'subject': '$' + options['subject']
                    },
                    'arrayOfDevices': {'$push': '$devices'},
                }
            },
            {
                '$project': {
                    '_id': False,
                    'month': '$_id.month',
                    'subject': '$_id.subject',
                    'countPerSubjectAndMonth': {'$size': '$arrayOfDevices'}
                }
            },
            {
                '$sort': {
                    'subject': DESCENDING,
                    'month': DESCENDING
                }
            },
            {
                '$group': {
                    '_id': {
                        'subject': '$subject'
                    },
                    'devices': {'$push': '$countPerSubjectAndMonth'},
                    'months': {'$push': '$month'}
                }
            },
            {
                '$project': {
                    '_id': False,
                    'subject': '$_id.subject',
                    'devices': True,
                    'months': True
                }
            }
        ]
        if 'receiverType' in options and options['event'] == 'Receive':
            pipeline[0]['$match']['type'] = options['receiverType']
        res = {
            'labels': list(calendar.month_name)[1:],
            'series': [],
            'data': []
        }
        a = self.aggregate(pipeline)
        for org in a:
            res['series'].append('Others' if org['subject'] is None else org['subject'])
            res['data'].append([0] * len(res['labels']))
            i = 0
            for pos in org['months']:
                res['data'][-1][pos - 1] = org['devices'][i]
                i += 1
        return res

    def aggregate(self, pipeline):
        return current_app.data.aggregate(self.resource_name, pipeline)['result']
