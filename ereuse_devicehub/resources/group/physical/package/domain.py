from collections import Iterable

from ereuse_devicehub.resources.domain import Domain
from ereuse_devicehub.resources.group.physical.domain import PhysicalDomain
from ereuse_devicehub.resources.group.physical.package.settings import PackageSettings


class PackageDomain(PhysicalDomain):
    resource_settings = PackageSettings

    @classmethod
    def remove_other_parents_of_type(cls, child_domain: Domain, children: Iterable):
        pass
