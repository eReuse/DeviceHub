from collections import Iterable

from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.domain import Domain
from ereuse_devicehub.resources.group.abstract.domain import AbstractDomain
from ereuse_devicehub.resources.group.abstract.lot.settings import Lot, LotSettings
from ereuse_devicehub.resources.group.physical.package.settings import Package
from ereuse_devicehub.resources.group.physical.pallet.settings import Pallet


class LotDomain(AbstractDomain):
    resource_settings = LotSettings

    @classmethod
    def inherit(cls, parent_id: str, parent_ancestors: list, child_domain: Domain, children: Iterable):
        """If children are lots inherits everything, and if children are packages or devices, inherit only lots."""
        child_resource_name = child_domain.resource_settings.resource_name()
        groups_inherit_lot = (Lot.resource_name,)
        if child_resource_name in Lot.resource_names:
            super().inherit(parent_id, parent_ancestors, child_domain, children)
        elif child_resource_name in Package.resource_names | Pallet.resource_names:
            full_children = cls._inherit(groups_inherit_lot, parent_id, parent_ancestors, child_domain, children)
            cls._update_inheritance_grandchildren(full_children, child_domain)
        elif child_resource_name in Device.resource_names:
            cls._inherit(groups_inherit_lot, parent_id, parent_ancestors, child_domain, children)
        else:
            raise KeyError('{} of {} cannot inherit a lot.'.format(children, child_resource_name))

    @classmethod
    def remove_other_parents_of_type(cls, child_domain: Domain, children: Iterable):
        pass
