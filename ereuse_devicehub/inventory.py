from datetime import datetime
from datetime import timedelta

from eve.auth import requires_auth
from flask import jsonify
from pydash import identity
from pydash import map_

from ereuse_devicehub.aggregation.aggregation import Aggregation
from ereuse_devicehub.header_cache import header_cache
from ereuse_devicehub.resources.device.component.settings import Component
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.utils import Naming


@header_cache(expires=5)
def inventory(db):
    """Returns several queries for the inventory widget of the dashboard."""
    requires_auth('resource')(identity)('devices')
    devices = InventoryDeviceAggregation()
    response = {
        'hardDrivesWithErrors': devices.hard_drives_with_errors(),
        'devicesMoreThanWeekWithoutBeingProcessed': devices.devices_more_than_without_being_processed(),
        'devicesNotFullyProcessed': devices.devices_not_fully_processed(),
        'placeholders': devices.placeholders()
    }
    return jsonify(response)


class InventoryAggregation(Aggregation):
    def _aggregate_count(self, pipeline, value_if_none=0) -> int:
        response = self._aggregate(pipeline)
        try:
            return response[0]['count']
        except IndexError:
            return value_if_none


class InventoryDeviceAggregation(InventoryAggregation):
    FINAL_EVENTS = ['devices:Ready', 'devices:Dispose']

    def __init__(self):
        super().__init__('devices')

    def devices_not_fully_processed(self):
        pipeline = [
            {
                '$match': {
                    '@type': {'$nin': list(Component.types)},
                }
            }
        ]
        pipeline += self._not_containing_events(self.FINAL_EVENTS)
        pipeline += [
            {
                '$group': {
                    '_id': None,
                    'count': {'$sum': 1}
                }
            },
            {
                '$project': {
                    '_id': False,
                    'count': True
                }
            }
        ]
        return self._aggregate_count(pipeline)

    def devices_more_than_without_being_processed(self, more_than: timedelta = timedelta(weeks=1)):
        EVENTS = map_(DeviceEventDomain.GENERIC_TYPES, lambda _, key: Naming.new_type(key, 'devices'))
        EVENTS += ['devices:Add', 'devices:Migrate']
        pipeline = [
            {
                '$match': {
                    '@type': {'$nin': list(Component.types)},
                    '_created': {'$lte': datetime.today() - more_than}
                }
            },
        ]
        pipeline += self._not_containing_events(EVENTS)
        pipeline += [
            {
                '$group': {
                    '_id': None,
                    'count': {'$sum': 1}
                }
            },
            {
                '$project': {
                    '_id': False,
                    'count': True
                }
            }
        ]
        return self._aggregate_count(pipeline)

    def hard_drives_with_errors(self) -> int:
        pipeline = [
            {
                '$match': {
                    '@type': 'HardDrive'
                }
            },
            {
                '$project': {
                    'erased': {
                        '$filter': {
                            'input': '$events',
                            'as': 'event',
                            'cond': {'$in': ['$$event.@type', ['devices:EraseBasic', 'devices:EraseSectors']]}
                        }
                    },
                    'disposed': {
                        '$filter': {
                            'input': '$events',
                            'as': 'event',
                            'cond': {'$in': ['$$event.@type', ['devices:Dispose']]}
                        }
                    }
                }
            },
            {
                '$match': {
                    'erased': {'$gte': ['$size', 1]},
                    'disposed': {'$size': 0},
                }
            },
            {
                '$group': {
                    '_id': None,
                    'count': {'$sum': 1}
                }
            }
        ]
        return self._aggregate_count(pipeline)

    def placeholders(self) -> int:
        pipeline = [
            {
                '$match': {
                    'placeholder': True
                }
            },
            {
                '$group': {
                    '_id': None,
                    'count': {'$sum': 1}
                }
            }
        ]
        return self._aggregate_count(pipeline)

    @staticmethod
    def _not_containing_events(events_type: list):
        return [
            {
                '$project': {
                    'contains': {
                        '$filter': {
                            'input': '$events',
                            'as': 'event',
                            'cond': {'$in': ['$$event.@type', events_type]}
                        }
                    }
                }
            },
            {
                '$match': {
                    'contains': {'$size': 0}
                }
            }
        ]
