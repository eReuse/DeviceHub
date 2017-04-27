from ereuse_devicehub.resources.group.abstract.lot.domain import LotDomain
from ereuse_devicehub.resources.group.abstract.lot.incoming_lot.settings import IncomingLotSettings


class IncomingLotDomain(LotDomain):
    resource_settings = IncomingLotSettings
    pass
