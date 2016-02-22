import calendar
import datetime

from flask import current_app
from pymongo import DESCENDING


class Aggregation:
    def __init__(self, resouce_name):
        self.resource_name = resouce_name

    def number_events(self, params: dict):
        """
        Counts the number of events performed of type event_type, grouped by horizontal_axis and optionally
        with the series

        :param horizontal_axis:
        :param event_type:
        :param series:
        :return:
        """
        number_events = API['number_events']
        for type, key in params.items():
            if type == 'filter':
                value = key['value']
                key = key['key']
            values = number_events[type][key]

    def number_devices_events(self):
        pipeline = [
            {
                '$match': {
                    '@type': 'Receive',
                    'type': 'CollectionPoint',
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
                        'receiverOrganization': '$receiverOrganization'
                    },
                    'arrayOfDevices': {'$push': '$devices'},
                }
            },
            {
                '$project': {
                    '_id': False,
                    'month': '$_id.month',
                    'receiverOrganization': '$_id.receiverOrganization',
                    'countPerOrganizationAndMonth': {'$size': '$arrayOfDevices'}
                }
            },
            {
                '$sort': {
                    'receiverOrganization': DESCENDING,
                    'month': DESCENDING
                }
            },
            {
                '$group': {
                    '_id': {
                        'receiverOrganization': '$receiverOrganization'
                    },
                    'devices': {'$push': '$countPerOrganizationAndMonth'},
                    'months': {'$push': '$month'}
                }
            },
            {
                '$project': {
                    '_id': False,
                    'receiverOrganization': '$_id.receiverOrganization',
                    'devices': True,
                    'months': True
                }
            }


        ]
        res = {
            'labels': list(calendar.month_name)[1:],
            'series': [],
            'data': []
        }
        a = self.aggregate(pipeline)
        for org in a:
            res['series'].append(org['receiverOrganization'])
            res['data'].append([0] * len(res['labels']))
            i = 0
            for pos in org['months']:
                res['data'][-1][pos - 1] = org['devices'][i]
                i += 1
        return res



    def aggregate(self, pipeline):
        return current_app.data.aggregate(self.resource_name, pipeline)['result']

    def mix_and_aggregate(self, group, match, project, sort):
        pipeline = []
        if match:
            pipeline.append({'$match': match})
        if group:
            pipeline.append({'$group': group})
        if sort:
            pipeline.append({'$sort': sort})
        if project:
            pipeline.append({'$project': project})
        return self.aggregate(pipeline)


API = {
    'number_events': {
        'series': {
            'organization': ('toOrganization', 'fromOrganization', 'byOrganization'),
            'user': ('to', 'from', 'by'),
            'place': ('place',)
        },
        'filter': {
            '@type': ('@type',)
        },
        'xAxis': {
            '_created': ('_created',)
        }
    }
}
