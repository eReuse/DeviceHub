from collections import Iterable
from typing import List, Set, Type

from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.domain import Domain
from ereuse_devicehub.resources.group.abstract.domain import AbstractDomain
from ereuse_devicehub.resources.group.abstract.lot.settings import Lot, LotSettings
from ereuse_devicehub.resources.group.domain import Perms
from ereuse_devicehub.resources.group.physical.package.settings import Package
from ereuse_devicehub.resources.group.physical.pallet.settings import Pallet


class LotDomain(AbstractDomain):
    resource_settings = LotSettings

    @classmethod
    def inherit(cls, parent_id: str, parent_ancestors: list, child_domain: Type[Domain], children: Set[str],
                parent_perms: Perms = None, accounts_to_remove: List[str] = None):
        """
        As GroupDomain.inherit, but not inheriting places when children are packages, devices or pallets.
        Note that this is only executed when the parent is a lot.

        We do this because we want for packages, devices and pallets to only be assigned in a place when they are
        explicitly assigned, and not when they are moved or added into a lot or when a lot
        is added to a place, because otherwise their places could accidentally change when playing with lots. For
        example, if a device is in a warehouse and is added to a lot that is somewhere else, the device would
        magically change its location. We want to have explicit confirmation from the user that the device
        moved to where it needs to be (potentially the place where the lot is in).
        """
        child_resource_name = child_domain.resource_settings.resource_name()
        groups_inherit_lot = (Lot.resource_name,)
        if child_resource_name in Lot.resource_names:
            super().inherit(parent_id, parent_ancestors, child_domain, children, parent_perms, accounts_to_remove)
        elif child_resource_name in Package.resource_names | Pallet.resource_names:
            full_children = cls._inherit(groups_inherit_lot, parent_id, parent_ancestors, child_domain, children,
                                         parent_perms, accounts_to_remove)
            cls._update_inheritance_grandchildren(full_children, child_domain, parent_perms, accounts_to_remove)
        elif child_resource_name in Device.resource_names:
            cls._inherit(groups_inherit_lot, parent_id, parent_ancestors, child_domain, children, parent_perms,
                         accounts_to_remove)
        else:
            raise KeyError('{} of {} cannot inherit a lot.'.format(children, child_resource_name))

    @classmethod
    def remove_other_parents_of_type(cls, new_parent_id: str, child_domain: Domain, children: Iterable):
        pass
