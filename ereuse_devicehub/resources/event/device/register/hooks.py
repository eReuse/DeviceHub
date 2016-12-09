from bson import json_util
from ereuse_devicehub.exceptions import InnerRequestError
from ereuse_devicehub.resources.device.component.domain import ComponentDomain
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.device.exceptions import DeviceNotFound, NoDevicesToProcess
from ereuse_devicehub.resources.event.device.register.settings import Register
from ereuse_devicehub.rest import execute_post_internal, execute_delete
from ereuse_devicehub.utils import Naming
from eve.methods.delete import deleteitem_internal
from flask import current_app as app


def post_devices(registers: list):
    """
    Main function for Register. For the given devices, POST the new ones.

    If there is an unexpected error (device has a bad field, for example), it undoes all posted devices. In db terms,
    the commit is all the registers.

    If the function is called by post_internal(), as the method keeps the reference of the passed in devices, the
    caller will see how their devices are replaced by the db versions, plus a 'new' property acting as a flag
    to indicate if the device is new or not.

    :raise InnerRequestError: for any error provoked by a failure in the POST of a device (except if the device already
        existed). It carries the original error sent by the POST.
    :raise NoDevicesToProcess: Raised to avoid creating empty registers, that actually did not POST any device
    """
    log = []
    try:
        for register in registers:
            caller_device = register['device']  # Keep the reference from where register['device'] points to
            _execute_register(caller_device, register.get('created'), log)
            register['device'] = caller_device['_id']
            if 'components' in register:
                caller_components = register['components']
                register['components'] = []
                for component in caller_components:
                    component['parent'] = caller_device['_id']
                    _execute_register(component, register.get('created'), log)
                    if component['new']:  # todo put new in g., don't use device
                        register['components'].append(component['_id'])
                if caller_device['new']:
                    set_components(register)
                elif not register['components']:
                    raise NoDevicesToProcess()
    except Exception as e:
        for device in reversed(log):  # Rollback
            deleteitem_internal(Naming.resource(device['@type']), device)
        raise e
    else:
        from ereuse_devicehub.resources.hooks import set_date
        set_date(None, registers)  # Let's get the time AFTER creating the devices


def _execute_register(device: dict, created: str, log: list):
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
    device['hid'] = 'dummy'
    new = True
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
        except DeviceNotFound:
            raise e
    else:
        log.append(db_device)
    device.clear()
    device.update(db_device)
    device['new'] = new  # Note that the device is 'cleared' before
    return db_device


def _get_existing_device(e: InnerRequestError) -> dict:
    """Gets the device from a special formatted cerberus error."""
    device = None
    for field in 'hid', '_id', 'model':  # unique fields
        if field in e.body['_issues']:
            try:
                for error in e.body['_issues'][field]:
                    try:
                        device = json_util.loads(error)['NotUnique']
                    except (ValueError, KeyError):
                        pass
                    else:
                        break
            except (ValueError, KeyError):
                raise DeviceNotFound()
    if not device:
        raise DeviceNotFound()
    return device


def set_components(register):
    """Sets the new devices to the materialized attribute 'components' of the parent device."""
    app.data.driver.db['devices'].update(
        {'_id': register['device']},
        {'$set': {'components': register['components']}}
    )


def delete_device(_, register):
    if register.get('@type') == Register.type_name:
        for device_id in [register['device']] + register.get('components', []):
            execute_delete(Naming.resource(DeviceDomain.get_one(device_id)['@type']), device_id)
