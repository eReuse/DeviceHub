from collections import Iterable

from ereuse_devicehub.resources.domain import Domain
from ereuse_devicehub.resources.group.physical.domain import PhysicalDomain
from ereuse_devicehub.resources.group.physical.package.settings import PackageSettings


class PackageDomain(PhysicalDomain):
    resource_settings = PackageSettings
