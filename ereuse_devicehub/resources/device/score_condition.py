import copy
from os.path import dirname, join, realpath
from warnings import filterwarnings, resetwarnings

from rpy2.rinterface import RRuntimeWarning
from rpy2.robjects import DataFrame, ListVector, r

from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.export.export import SpreadsheetTranslator
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.condition import condition as condition_schema
from ereuse_devicehub.resources.device.domain import DeviceDomain


class ScorePriceBase:
    ROUND_DECIMALS = 2

    def __init__(self, app) -> None:
        self.app = app
        self.translator = SpreadsheetTranslator(brief=False)
        for package in 'dplyr', 'data.table', 'stringr':
            kwargs = {'lib_loc': app.config['R_PACKAGES_PATH']} if app.config['R_PACKAGES_PATH'] else {}
            r.require(package, **kwargs)

    def compute(self, device_id: str, condition: dict) -> (DataFrame, dict):
        device = DeviceDomain.get_one(device_id)
        device['components'] = DeviceDomain.get_full_components(device['components'])
        device['condition'] = copy.deepcopy(condition)
        keys, values = self.translator.translate([device])
        data = {key.replace(' ', '.').replace('(', '.').replace(')', '.'): val for key, val in zip(keys, values)}
        return DataFrame(data), condition

    def _parse_response(self, response, device_id):
        data, status = tuple(response)
        status = int(status[0])
        if status != 0:
            raise ScorePriceError('{} couldn\'t be computed for device {}'.format(self.__class__.__name__, device_id))
        return {name: data[i][0] for i, name in enumerate(data.names)}


class Score(ScorePriceBase):
    def __init__(self, app) -> None:
        filterwarnings('ignore', category=RRuntimeWarning)
        super().__init__(app)
        self.path = join(dirname(realpath(__file__)), 'score', 'RLanguage')

        r.source(join(self.path, 'R', 'RdeviceScore_Utils.R'))
        r.source(join(self.path, 'R', 'RdeviceScore.R'))
        # This is the function we call
        self.compute_score = r("""
                function (input){
                    return (deviceScoreMainServer(input)) 
                }""")
        resetwarnings()

    def compute(self, device_id: str, condition: dict) -> dict:
        data, _condition = super().compute(device_id, condition)
        param = ListVector({
            'pathApp': self.path,
            'sourceData': data,
            'simulation': '2',
            'versionSchema': 'v021',
            'versionScore': 'v2-2017-09-20'
        })
        result = self._parse_response(self.compute_score(param), device_id)
        _condition['general'] = {
            'score': round(result['Score'], self.ROUND_DECIMALS),
            'range': result['Range']
        }
        _condition['scoringSoftware'] = {
            'label': 'ereuse.org',
            'version': '1.0'
        }
        _condition['components'] = {
            'ram': round(result['Ram.score'], self.ROUND_DECIMALS),
            'processors': round(result['Processor.score'], self.ROUND_DECIMALS),
            'hardDrives': round(result['Drive.score'], self.ROUND_DECIMALS)
        }
        # Validate that the returned data complies with the schema
        validator = self.app.validator(condition_schema)
        if not validator.validate(_condition):
            t = 'RDeviceScore wrong condition:\n'
            t += 'Device {} of {}\n'.format(device_id, AccountDomain.requested_database)
            t += 'Condition is: {}'.format(_condition)
            raise ScorePriceError(t)
        return _condition


class Price(ScorePriceBase):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.path = join(dirname(realpath(__file__)), 'price', 'RLanguage')

        r.source(join(self.path, 'R', 'RDevicePrice_Utils.R'))
        r.source(join(self.path, 'R', 'RDevicePrice.R'))
        # This is the function we call
        self.compute_price = r("""
                function (input){
                    return (devicePriceMain(input))
                }""")

    def compute(self, device_id: str, condition: dict):
        data, condition = super().compute(device_id, condition)


class ScorePriceError(StandardError):
    pass
