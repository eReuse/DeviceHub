from collections import Iterable

from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.domain import Domain
from ereuse_devicehub.resources.group.abstract.domain import AbstractDomain
from ereuse_devicehub.resources.group.abstract.lot.settings import Lot
from ereuse_devicehub.resources.group.abstract.settings import AbstractSettings
from ereuse_devicehub.resources.group.domain import GroupDomain
from ereuse_devicehub.resources.group.physical.package.settings import Package


class LotDomain(AbstractDomain):
    resource_settings = AbstractSettings

    @classmethod
    def inherit(cls, parent_label: str, parent_ancestors: list, child_domain: Domain, children: Iterable):
        """If children are lots inherits everything, and if children are packages or devices, inherit only lots."""
        child_resource_name = child_domain.resource_settings.resource_name()
        if child_resource_name == Lot.resource_name:
            super().inherit(parent_label, parent_ancestors, child_domain, children)
        elif child_resource_name == Package.resource_name or child_resource_name == Device.resource_name:
            full_children = cls._inherit((Lot.resource_name,), parent_label, parent_ancestors, child_domain, children)
            if issubclass(child_domain, GroupDomain):
                cls._update_inheritance_grandchildren(full_children, child_domain)
        else:
            raise KeyError('{} of {} cannot inherit a lot.'.format(children, child_resource_name))

    @classmethod
    def remove_other_parents_of_type(cls, child_domain: Domain, children: Iterable):
        pass
