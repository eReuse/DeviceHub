from ereuse_devicehub.resources.group.abstract.lot.domain import LotDomain
from ereuse_devicehub.resources.group.abstract.lot.outgoing_lot.settings import OutgoingLotSettings


class OutgoingLotDomain(LotDomain):
    resource_settings = OutgoingLotSettings
    pass
