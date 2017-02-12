from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.group.physical.settings import PhysicalSettings


class PhysicalDomain(GroupDomain):
    resource_settings = PhysicalSettings
    foreign_key_in_device = None

    @classmethod
    def device_set_group(cls, device_id, group_id: str):
        cls._remove_device_from_group(device_id)  # Let's see remove any group the device had
        # And we set ours to the device
        update_dict = {'$set': {'parent': group_id}}
        DeviceDomain.update_one_raw({'_id': device_id}, update_dict)

    @staticmethod
    def device_unset_group(cls, device_id: str):
        DeviceDomain.update_one_raw({'_id': device_id}, {'$unset': {cls.foreign_key: ''}})
