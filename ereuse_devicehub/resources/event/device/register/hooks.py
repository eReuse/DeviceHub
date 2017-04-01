from contextlib import suppress

from bson import json_util
from eve.methods.delete import deleteitem_internal
from pydash import is_empty
from pydash import pick

from ereuse_devicehub.exceptions import InnerRequestError, SchemaError
from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.computer.hooks import update_materialized_computer
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.exceptions import DeviceNotFound, NoDevicesToProcess
from ereuse_devicehub.resources.event.device.register.settings import Register
from ereuse_devicehub.rest import execute_post_internal, execute_delete
from ereuse_devicehub.utils import Naming


def post_devices(registers: list):
    """
    Main function for Register. For the given devices, POST the new ones. This method rollbacks the database when
    raising exceptions, like when no device has been POSTed.

    If the function is called by post_internal(), as the method keeps the reference of the passed in devices, the
    caller will see how their devices are replaced by the db versions, plus a 'new' property acting as a flag
    to indicate if the device is new or not.

    If a device exists, the input device is replaced by the version of the database, loosing any change the
    input device was introducing (except benchmarks, which are updated). See `_execute_register` for more info.

    :raise InnerRequestError: for any error provoked by a failure in the POST of a device (except if the device already
        existed). It carries the original error sent by the POST.
    :raise NoDevicesToProcess: Raised to avoid creating empty registers, that actually did not POST any device
    """
    log = []
    register = registers[0]
    try:
        device = register['device']  # register['device'] will be only the _id later
        if 'parent' in register:  # If device is a component which we are manually setting its parent
            device['parent'] = register['parent']
        register['deviceIsNew'] = device_is_new = _execute_register(device, register.get('created'), log)
        register['device'] = device['_id']
        components_created = []  # Note that components_created it doesn't need to be equal to register['comp.']
        for component in register.get('components', []):
            # Although we set materialized 'parent' in component after (in add_components), this one is needed
            # to help in case of a new component that cannot generate HID, linking it to its parent
            component['parent'] = device['_id']
            if _execute_register(component, register.get('created'), log):  # Component is new
                components_created.append(component['_id'])
        register['components'] = components_created  # We only keep in the event the new components
        if not device_is_new and is_empty(components_created):
            t = 'Device {} and components {} already exist.'.format(register['device'], register['components'])
            raise NoDevicesToProcess(t)
        if 'parent' in register:
            # If our *device* is a component itself, we need to inherit from its parent
            update_materialized_computer(register['parent'], [device['_id']], add=True)
        # We inherit groups to new components and materialize device - components relationships
        update_materialized_computer(device, components_created, add=True)
    except Exception as e:
        for device in reversed(log):  # Rollback
            deleteitem_internal(Naming.resource(device['@type']), device)
        raise e
    else:
        from ereuse_devicehub.resources.hooks import set_date
        set_date(None, registers)  # Let's get the time AFTER creating the devices


def _execute_register(device: dict, created: str, log: list) -> bool:
    """
    Tries to POST the device and updates the `device` dict with the resource from the database; if the device could
    not be uploaded the `device` param will contain the database version of the device, not the inputting one. This is
    because the majority of the information of a device is immutable (in concrete the fields used to compute
    the ETAG).

    :param device: Inputting device. It is replaced (keeping the reference) with the db version.
    :param created: Set the _created value to be the same for the device as for the register
    :param log: A log where to append the resulting device if execute_register has been successful
    :raise InnerRequestError: any internal error in the POST that is not about the device already existing.
    """
    try:
        if created:
            device['created'] = created
        db_device = execute_post_internal(Naming.resource(device['@type']), device)
    except InnerRequestError as e:
        new = False
        try:
            db_device = _get_existing_device(e)
            # We add a benchmark todo move to another place?
            device['_id'] = db_device['_id']
            ComponentDomain.benchmark(device)
            external_synthetic_id_fields = pick(device, *DeviceDomain.external_synthetic_ids)
            # If the db_device was a placeholder
            # We want to override it with the new device
            if db_device.get('placeholder', False):
                # Eve do not generate defaults from sub-resources
                # And we really need the placeholder default set, specially when
                # discovering a device
                device['placeholder'] = False
                # We create hid when we validate (wrong thing) so we need to manually set it here as we won't
                # validate in this db operation
                device['hid'] = DeviceDomain.hid(device['manufacturer'], device['serialNumber'], device['model'])
                DeviceDomain.update_one_raw(db_device['_id'], {'$set': device})
            elif not is_empty(external_synthetic_id_fields):
                # External Synthetic identifiers are not intrinsically inherent
                # of devices, and thus can be added later in other Snapshots
                # Note that the device / post and _get_existing_device() have already validated those ids
                DeviceDomain.update_one_raw(db_device['_id'], {'$set': external_synthetic_id_fields})
        except DeviceNotFound:
            raise e
    else:
        new = True
        log.append(db_device)
    device.clear()
    device.update(db_device)
    return new


def _get_existing_device(e: InnerRequestError) -> dict:
    """
    Gets the device encoded in the InnerRequestError after ensuring integrity in the errors.

    Only accepted errors are about already existing unique id fields (like _id or hid), as they are the only ones
    that hint an already existing device.

    @raise MismatchBetweenUid: When the unique ids point at different devices, this is usually a mispelling error
    by the user, as some uids can be entered manually.
    @raise DeviceNotFound: There is not an uid error or it is not well formatted
    """
    devices = []
    for field in DeviceDomain.uid_fields | {'model'}:  # Model is used when matching in components with parents
        for error in e.body['_issues'].get(field, []):
            with suppress(ValueError, KeyError):
                device = json_util.loads(error)['NotUnique']
                if not is_empty(devices) and device['_id'] != devices[-1][1]['_id']:
                    raise MismatchBetweenUid(field, device['_id'], devices[-1][1]['_id'], devices[-1][0])
                devices.append((field, device))
    if is_empty(devices):
        raise DeviceNotFound()
    return devices[-1][1]


def delete_device(_, register):
    if register.get('@type') == Register.type_name:
        for device_id in [register['device']] + register.get('components', []):
            execute_delete(Naming.resource(DeviceDomain.get_one(device_id)['@type']), device_id)


class MismatchBetweenUid(SchemaError):
    def __init__(self, field, device_id, other_device_id, other_field):
        self.field = field
        self.device_id = device_id
        self.other_device_id = other_device_id
        self.other_field = other_field
        formatting = [self.device_id, self.other_field, self.other_device_id]
        message = 'This ID identifies the device {} but the {} identifies the device {}'.format(*formatting)
        super(MismatchBetweenUid, self).__init__(field, message)
