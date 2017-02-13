from ereuse_devicehub.resources.group.abstract.settings import AbstractSettings
from ereuse_devicehub.resources.group.domain import GroupDomain


class AbstractDomain(GroupDomain):
    resource_settings = AbstractSettings
