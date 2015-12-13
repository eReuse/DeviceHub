from bson import json_util
from eve.methods.delete import deleteitem_internal

from app.app import app
from app.device.exceptions import DeviceNotFound, NoDevicesToProcess
from app.exceptions import InnerRequestError
from app.utils import get_resource_name
from app.rest import execute_post


def post_devices(registers: list):
    """
    Main function for Register. For the given devices, POST the new ones.

    If there is an unexpected error (device has a bad field, for example), it undoes all posted devices. In db terms,
        the commit is all the registers.

    If the function is called by post_internal(), as the method keeps the reference of the passed in devices, the
        caller will see how their devices are replaced by the db versions, plus a 'new' property acting as a flag
        to indicate if the device is new or not.

    :type registers: list
    :raises InnerRequestError: for any error provoked by a failure in the POST of a device (except if the device already
        existed). It carries the original error sent by the POST.
    """
    log = []
    for register in registers:
        caller_device = register['device']  # Keep the reference from where register['device'] points to
        _execute_register(caller_device, log, True)
        register['device'] = caller_device['_id']  # Change the reference of register['device'], but not caller_device
        if 'components' in register:
            caller_components = register['components']
            register['components'] = []
            for component in caller_components:
                component['parent'] = caller_device['_id']
                _execute_register(component, log)
                if 'new' in component:  # todo put new in g., don't use device
                    register['components'].append(component['_id'])
            if not register['components'] and 'new' not in caller_device:
                _abort(
                    log)  # If we have not POST neither any component and any device there is no reason for register to exist
            if 'new' in caller_device:
                set_components(register)


def _execute_register(device: dict, log: list, force_new=False):
    device['hid'] = 'dummy'
    try:
        db_device = execute_post(get_resource_name(device['@type']), device)
    except InnerRequestError as e:
        if force_new:
            raise e #todo remove force_new stuff to let existing devices to get more than one snapshot, use Add/Remoe...
        new = False
        try:
            db_device = _get_existing_device(e)
        except DeviceNotFound:
            _abort(log, e)
    else:
        log.append(db_device)
        new = True
    device.clear()
    device.update(
        db_device)  # We do not assign so we preserve the reference todo db_device just have extra_post_fields, not all fields of device
    if new:
        device['new'] = new


def _get_existing_device(e):
    device = None
    for field in 'hid', 'pid', 'model':  # unique fields
        if field in e.body['_issues']:
            try:
                device = json_util.loads(e.body['_issues'][field])['NotUnique']
            except ValueError:  # it can be an unique field but the
                raise DeviceNotFound()
    if not device:
        raise DeviceNotFound()
    return device


def set_components(register):
    """
    Sets the new devices to the materialized attribute 'components' of the parent device.
    """
    app.data.driver.db['devices'].update(
        {'_id': register['device']},
        {'$set': {'components': register['components']}}
    )


def _abort(log, e: Exception = NoDevicesToProcess()):
    for device in reversed(log):
        deleteitem_internal(get_resource_name(device['@type']), device)
    raise e
