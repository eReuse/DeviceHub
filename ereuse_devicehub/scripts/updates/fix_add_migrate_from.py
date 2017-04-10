from datetime import datetime

from bson import ObjectId
from flask import current_app
from pydash import filter_
from pydash import map_

from ereuse_devicehub.resources.device.component.settings import Component
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.scripts.updates.re_materialize_events_in_devices import ReMaterializeEventsInDevices


class FixAddMigrateFrom(ReMaterializeEventsInDevices):
    """Re-does internally a Migrate that was erroniously partly-erased"""
    def execute(self, database):
        if database == 'alencop':
            DeviceEventDomain.delete({"_id": ObjectId('58e283091f632f56a18ca413')})
            ids = list(range(1348, 1448))
            ids = [str(_id) for _id in ids]
            devices = DeviceDomain.get({'_id': {'$in': ids}})
            non_components = filter_(devices, lambda x: x['@type'] not in Component.types)
            components = filter_(devices, lambda x: x['@type'] in Component.types)
            migrate = {
                '_id': ObjectId('58e283091f632f56a18ca413'),
                'label': 'BCN Activa a Alencop Març',
                'events': [],
                'devices': map_(non_components, '_id'),
                'components': map_(components, '_id'),
                'from': "https://devicehub.ereuse.org/circuit-reutilitza-cat/events/devices/migrate/569c285e75d9351f7f82f668",
                "comment": "Transferència de la donació de Barcelona Activa al Circuit Pangea que Alencop va recollir.",
                "label": "Barcelona Activa (Març) a Alencop.",
                '_updated': datetime.strptime("2017-04-03T17:14:37", current_app.config['DATE_FORMAT']),
                '_created': datetime.strptime("2017-04-03T17:14:37", current_app.config['DATE_FORMAT']),
                '@type': 'devices:Migrate'
            }
            DeviceEventDomain.insert(migrate)
            super(FixAddMigrateFrom, self).execute(database)
