from ereuse_devicehub.resources.group.physical.domain import PhysicalDomain
from ereuse_devicehub.resources.group.physical.package.settings import PackageSettings


class PackageDomain(PhysicalDomain):
    resource_settings = PackageSettings
    foreign_key_in_device = 'package'
