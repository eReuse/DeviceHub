import json
from contextlib import suppress
from typing import List

from flask import Request, Response, current_app as app, g, request

from ereuse_devicehub.exceptions import InnerRequestError, SchemaError
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.score_condition import ScorePriceError, ScorePriceNotSuitableError
from ereuse_devicehub.resources.domain import ResourceNotFound
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.domain import EventNotFound
from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.rest import execute_delete, execute_patch
from ereuse_utils.naming import Naming
from .snapshot import Snapshot, SnapshotWithoutComponents


def on_insert_snapshot(items):
    for item in items:
        if 'label' in item:
            item['device']['labelId'] = item['label']  # todo as we do not update the values of a device,
        # todo we will never update, thus materializing new label ids
        if item['snapshotSoftware'] == 'Workbench':
            snapshot = Snapshot(item['device'], item['components'], item.get('created'), item.get('parent'))
        else:  # In App or web we do not ask for component info
            snapshot = SnapshotWithoutComponents(item['device'], created=item.get('created'), parent=item.get('parent'))
        item['events'] = [new_events['_id'] for new_events in snapshot.execute()]
        item['device'] = snapshot.device['_id']
        item['components'] = [component['_id'] for component in snapshot.components]
        item['unsecured'] = snapshot.unsecured
        from ereuse_devicehub.resources.hooks import set_date
        set_date(None, items)  # Let's get the time AFTER creating the other events
        g.dh_snapshot = snapshot


def save_request(items):
    """
    Saves the original request in a string in the 'request' field in json for debugging purposes.

    Warning: This method does not support bulk inserts.
    """
    items[0]['request'] = request.data.decode()


def materialize_test_hard_drives(_):
    """Materializes the ``tests`` property of the hard-drive with the new tests from the snapshot."""
    for i, test_hard_drives in getattr(g.dh_snapshot, 'test_hard_drives', []):
        _materialize_event_in_device(test_hard_drives, 'tests')


def materialize_erasures(_):
    """Materializes the ``erasures`` property of the hard-drive with the new erasures from the snapshot."""
    for i, erase_basic in getattr(g.dh_snapshot, 'erasures', []):
        _materialize_event_in_device(erase_basic, 'erasures')


def _materialize_event_in_device(event, field_name):
    DeviceDomain.update_one_raw(event['device'], {'$push': {field_name: event['_id']}})


def compute_condition_price_and_materialize_in_device(snapshots: list):
    """Computes condition and pricing and then saves it in snapshot and materializes in device."""
    for snapshot in snapshots:
        try:
            # condition and pricing may fail as they are executing external unstable libraries
            # Pricing needs condition, so if condition fails there is no need to execute pricing
            device = app.score.get_device(snapshot['device'], snapshot.get('condition', {}))
            snapshot['condition'] = app.score.compute(device)
            snapshot['pricing'] = app.price.compute(device)
            q = {'$set': {'condition': snapshot['condition'], 'pricing': snapshot['pricing']}}
            DeviceEventDomain.update_one_raw(snapshot['_id'], q)
        except ScorePriceNotSuitableError:
            # Note that we silent some expected exceptions
            pass
        except (ScorePriceError, ScorePriceNotSuitableError) as e:
            app.logger.info(e)
        # Materialize to device if needed
        if 'condition' in snapshot or 'pricing' in snapshot:
            q = {'$set': {'condition': snapshot.get('condition', {}), 'pricing': snapshot.get('pricing', {})}}
            DeviceDomain.update_one_raw(snapshot['device'], q)


def delete_events(_, snapshot: dict):
    """Deletes the events that were created with the snapshot."""
    if snapshot.get('@type') == 'devices:Snapshot':
        for event_id in snapshot['events']:
            with suppress(EventNotFound):
                # If the first event is Register, erasing the device will erase the rest of events
                event = DeviceEventDomain.get_one(event_id)
                try:
                    execute_delete(Naming.resource(event['@type']), event['_id'])
                except InnerRequestError as e:
                    if e.status_code != 404:
                        raise e


SNAPSHOT_SOFTWARE = {
    'DDI': 'Workbench',
    'Scan': 'AndroidApp',
    'DeviceHubClient': 'Web'
}


def move_id_remove_logical_name(payload: Request):
    """Moves the _id and pid from the snapshot to the inner device of the snapshot, as a hotfix for Workbench's bug"""
    # todo workbench hotfix
    snapshot = payload.get_json()
    for identifier in '_id', 'pid', 'gid', 'hid', 'rid':
        with suppress(Exception):
            snapshot['device'][identifier] = snapshot.pop(identifier)
    with suppress(Exception):
        snapshot['snapshotSoftware'] = SNAPSHOT_SOFTWARE[snapshot['snapshotSoftware']]
    with suppress(Exception):
        for component in snapshot['components']:
            if 'logical_name' in component:
                del component['logical_name']


def add_to_group(snapshots: List[dict]):
    """Adds the device to the group, if it was not there before."""
    for snapshot in snapshots:
        if 'group' in snapshot:
            try:
                g_type = snapshot['group']['@type']
                resource_name = Naming.resource(g_type)
                group = GroupDomain.children_resources[resource_name].get_one(snapshot['group']['_id'])
                # We add the device in the group if it didn't exist already
                if snapshot['device'] not in group['children'].get('devices', []):
                    group['children'].setdefault('devices', []).append(snapshot['device'])
                    group_patch = {'@type': g_type, 'children': group['children']}
                    execute_patch(resource_name, group_patch, group['_id'])
            except (ResourceNotFound, InnerRequestError) as e:
                g.dh_snapshot_add_to_group = SchemaError(field='group',
                                                         message='We created the Snapshot, but we couldn\'t add '
                                                                 'the devices to the group {} because {}'
                                                         .format(snapshot['group']['_id'], e))


def return_202_when_could_not_add_to_group(response: Response):
    # This is executed in an after_request
    if 'dh_snapshot_add_to_group' in g:
        response.status_code = 202
        data = json.loads(response.data.decode())
        e = g.dh_snapshot_add_to_group.to_dict()
        data['_warning'] = e['_error']
        data['_status'] = 'WARN'
        data.update(data)
        response.data = json.dumps(data)
    return response
