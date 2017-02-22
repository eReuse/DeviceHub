import calendar
import datetime

from flask import current_app
from pymongo import DESCENDING
from werkzeug.datastructures import ImmutableList

from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.resources.device.component.settings import Component
from ereuse_devicehub.utils import cache


class Aggregation:
    """
    The methods of the Aggregation class return aggregated data ready to be presented with Chart.js and similar.
    """

    # For how much time is the data cached?
    CACHE_TIMEOUT = 1 * 60  # 1 minute

    def __init__(self, resouce_name):
        self.resource_name = resouce_name

    def devices_per_event_subject_month(self, options):
        """
        Returns the number of devices per event, subject and month.

        Subject is the series of the graph, and
        :param options:
        :return:
        """
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
        a = self._aggregate(ImmutableList(pipeline))
        for org in a:
            res['series'].append('Others' if org['subject'] is None else org['subject'])
            res['data'].append([0] * len(res['labels']))
            i = 0
            for pos in org['months']:
                res['data'][-1][pos - 1] = org['devices'][i]
                i += 1
        return res

    def discovered_devices(self, group=None):
        pipeline = [
            {
                '$match': {
                    '@type': {'$nin': list(Component.types)},
                }
            },
            {
                '$group': {
                    '_id': '$placeholder',
                    'number': {'$sum': 1}
                }
            }
        ]
        a = self._aggregate(ImmutableList(pipeline))
        res = {
            'result': a
        }
        return res

    @cache.memoize(timeout=CACHE_TIMEOUT)
    def _aggregate(self, pipeline):
        return current_app.data.aggregate(self.resource_name, pipeline)


class AggregationError(StandardError):
    status_code = 400
