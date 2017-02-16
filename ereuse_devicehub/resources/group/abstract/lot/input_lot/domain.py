from ereuse_devicehub.resources.group.abstract.lot.domain import LotDomain
from ereuse_devicehub.resources.group.abstract.lot.input_lot.settings import InputLotSettings


class InputLotDomain(LotDomain):
    resource_settings = InputLotSettings
    pass
