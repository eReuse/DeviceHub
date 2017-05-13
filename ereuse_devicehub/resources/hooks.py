from datetime import datetime, timezone

from bson import ObjectId
from flask import current_app, json
from pydash import pick
from requests import Response

from ereuse_devicehub.exceptions import RedirectToClient, StandardError, SchemaError
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.event.device import DeviceEventDomain
from ereuse_devicehub.resources.event.device.settings import DeviceEvent
from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.schema import RDFS
from ereuse_devicehub.utils import get_header_link


def redirect_on_browser(_, request, __):
    """
    Redirects the browsers to the client webApp.
    :param request:
    """
    if request.accept_mimetypes.accept_html:
        raise RedirectToClient()


def set_response_headers_and_cache(resource: str, _, payload: Response):
    """
    Sets JSON Header link referring to @type
    """
    if (payload._status_code == 200 or payload._status_code == 304) and resource is not None:
        data = json.loads(payload.data.decode(payload.charset))
        resource_type = resource
        try:
            resource_type = data['@type']
        except KeyError:
            if payload._status_code == 304:
                payload.cache_control.max_age = current_app.config['ITEM_CACHE']
        else:
            # If we are here it means it is an item endpoint, not a list (resource) endpoint
            payload.cache_control.max_age = current_app.config['ITEM_CACHE']
        payload.headers._list.append(get_header_link(resource_type))


def set_date(name: str, resources: dict):
    """Eve's date is not precise enough (up to seconds) for massive insertion of resources."""
    for resource in resources:
        if name != 'devices_snapshot' and name != 'devices_register':
            # Snapshot and Register will call this method on it's right time, setting name to None
            resource['_created'] = resource['_updated'] = resource.pop('created', datetime.utcnow())


def avoid_deleting_if_not_last_event_or_more_x_minutes(resource_name: str, _, lookup: dict):
    """
    Deleting breaks traceability, and we only allow it to **undo** a mistake, something that
    happens before X time.

    A better version of this could we to allow only superusers to delete independently of the timing,
    and this solves deleting stuff in GRD: send things in GRD after this timing has passed, and they
    won't be deleted.

    To avoid complications in deleting, we only allow it if the event is the last one applied to all its devices
    and components.

    Note that other hooks check other things and that this hook is combined (check time and check event) to avoid
    an extra get_one method.

    This hook needs to be executed in the PRE so it is only checked when the user makes DELETE, and not when it is
    done through deleteitem_internal, as some resources delete other resources (like Snapshot). In those cases,
    we do not want to a) get out of time before deleting an inner resource, b) in Snapshot inner resources are
    deleted prior Snapshot however Snapshot is the last event, which would cause error.
    """
    # Note that devices are only redirected to their first snapshot so this is going to be checked on there
    is_device_event = resource_name in DeviceEvent.resource_names
    if is_device_event:
        resource = DeviceEventDomain.get_one(ObjectId(lookup['_id']))
    elif resource_name in Device.resource_names:
        resource = DeviceDomain.get_one(lookup['_id'])
    else:
        return
    # Checks timing
    if datetime.now(timezone.utc) - resource['_created'] > current_app.config['TIME_TO_DELETE_RESOURCES']:
        raise TooLateToDelete()
    # Checks event is last
    if is_device_event:
        for device_id in DeviceEventDomain.devices_id(resource) + resource.get('components', []):
            device = DeviceDomain.get_one(device_id)
            if device['events'][0]['_id'] != resource['_id']:  # It is not the last event
                raise OnlyLastEventCanBeDeleted(device_id)


class TooLateToDelete(StandardError):
    """Error raised when a resource has been tried to be deleted too late."""
    status_code = 405  # Method not allowed

    def __init__(self):
        max_time = current_app.config['TIME_TO_DELETE_RESOURCES']
        message = 'You can only delete this before it has passed {}.'.format(max_time)
        super().__init__(message)


class OnlyLastEventCanBeDeleted(StandardError):
    status_code = 405  # Method not allowed

    def __init__(self, device_id: str):
        message = 'The event is not the last one for device {} so you can\'t delete it.'.format(device_id)
        super().__init__(message)


class MaterializeEvents:
    """
        Materializes some fields of the events in the affected device, benefiting searches. To keep minimum space,
        only selected fields are materialized (which you can check in the following tuple)
    """
    FIELDS = {
        '_id', '@type', 'label', 'date', 'incidence', 'secured', 'comment', 'success', 'error', 'type', 'receiver',
        'receiverOrganization', 'to', 'toOrganization', 'secured', 'byUser', 'geo', '_updated', 'snapshotSoftware'
    }
    # Let's materialize the events (test, erasure...) of the component to the parent, so we take 'parent'
    DEVICE_FIELDS = 'device', 'devices', 'parent', 'components'

    @classmethod
    def materialize_events(cls, resource: str, events: list):
        """Materializes the event in their devices and groups."""
        if resource in DeviceEvent.resource_names:
            for event in events:
                QUERY = {'$push': {'events': {'$each': [pick(event, *cls.FIELDS)], '$position': 0}}}
                cls._update_materializations(event, QUERY)

    @classmethod
    def dematerialize_event(cls, _, event: dict):
        """
        Removes the materializaitons of the event in its devices and groups, usually because the event is being deleted.
        """
        if event.get('@type', None) in DeviceEvent.types:
            QUERY = {'$pull': {'events': {'_id': event['_id']}}}
            cls._update_materializations(event, QUERY)

    @classmethod
    def _update_materializations(cls, event: dict, query: dict):
        """Updates the materializations in the devices and groups using *query*."""
        # Update in devices, including the parent and components
        devices_id = DeviceEventDomain.devices_id(event, cls.DEVICE_FIELDS)
        DeviceDomain.update_raw(devices_id, query)

        # Update in groups, if any
        for resource_name, labels in event.get('groups', {}).items():
            GroupDomain.children_resources[resource_name].update_raw(labels, query, key='label')


def check_type(_, resources: list):
    """Many hooks require a @type in the resources. This one guarantees it for the top resource."""
    for resource in resources:
        if resource.get('@type', None) not in RDFS.types:
            raise TypeIsInvalid('@type')


class TypeIsInvalid(SchemaError):
    message = '@type is missing or misspelled.'
