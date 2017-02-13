from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.group.physical.settings import PhysicalSettings


class PhysicalDomain(GroupDomain):
    resource_settings = PhysicalSettings
