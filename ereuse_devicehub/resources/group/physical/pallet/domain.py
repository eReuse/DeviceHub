from collections import Iterable

from ereuse_devicehub.resources.domain import Domain
from ereuse_devicehub.resources.group.physical.domain import PhysicalDomain
from ereuse_devicehub.resources.group.physical.pallet.settings import PalletSettings


class PalletDomain(PhysicalDomain):
    resource_settings = PalletSettings

    @classmethod
    def remove_other_parents_of_type(cls, child_domain: Domain, children: Iterable):
        """Removes other pallets and packages the resource may have."""
        query = {'$pull': {'ancestors': {'@type': 'Package'}}}
        child_domain.update_raw(children, query)
        super().remove_other_parents_of_type(child_domain, children)
