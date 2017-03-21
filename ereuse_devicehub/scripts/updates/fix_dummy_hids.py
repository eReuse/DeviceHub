from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.scripts.updates.update import Update


class FixDummyHids(Update):
    """
    Re-computes HID for devices that had 'dummy' on it. Luckily those devices were placeholders set with _id
    and didn't affect the selection of device algorithm.
    """
    def execute(self, database):
        for device in DeviceDomain.get({'hid': 'dummy'}):
            try:
                hid = DeviceDomain.hid(device['manufacturer'], device['serialNumber'], device['model'])
                DeviceDomain.update_one_raw(device['_id'], {'$set': {'hid': hid}})
            except KeyError:
                DeviceDomain.update_one_raw(device['_id'], {'$unset': {'hid': ''}, '$set': {'isUidSecured': False}})
