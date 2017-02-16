from ereuse_devicehub.resources.group.abstract.lot.domain import LotDomain
from ereuse_devicehub.resources.group.abstract.lot.output_lot.settings import OutputLotSettings


class OutputLotDomain(LotDomain):
    resource_settings = OutputLotSettings
    pass
