import contextlib
import itertools
from collections import defaultdict
from warnings import filterwarnings, resetwarnings

from rpy2.rinterface import NA_Real, RRuntimeWarning
from rpy2.robjects import DataFrame, ListVector, r

from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.export.export import SpreadsheetTranslator
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.condition import condition as condition_schema
from ereuse_devicehub.resources.device.computer.settings import Computer
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.pricing import pricing
from ereuse_devicehub.validation.validation import DeviceHubValidator


class ScorePriceBase:
    ROUND_DECIMALS = 2

    def __init__(self, app) -> None:
        self.app = app
        self.translator = SpreadsheetTranslator(brief=False)
        self.validator = NotImplementedError()
        with self.filter_warnings():
            kwargs = {'lib_loc': app.config['R_PACKAGES_PATH']} if app.config['R_PACKAGES_PATH'] else {}
            r.library('Rdevicescore', **kwargs)

    def compute(self, device_id: str, condition: dict) -> DataFrame:
        # We can't compute empty conditions or anything that is not a computer
        if not condition:
            raise ScorePriceNotSuitableError()
        device = DeviceDomain.get_one(device_id)
        if device['@type'] != Computer.type_name:
            raise ScorePriceNotSuitableError()
        device['components'] = DeviceDomain.get_full_components(device['components'])
        device['condition'] = condition
        keys, values = self.translator.translate([device])
        data = {key.replace(' ', '.').replace('(', '.').replace(')', '.'): val for key, val in zip(keys, values)}
        return DataFrame(data)

    @staticmethod
    def _parse_response(data):
        return {name: data[i][0] for i, name in enumerate(data.names)}

    def _validate(self, validator: DeviceHubValidator, condition: dict, device_id: str):
        if not validator.validate(condition):
            t = '{} wrong condition:\n'.format(self.__class__.__name__)
            t += 'Device {} of {}\n'.format(device_id, AccountDomain.requested_database)
            t += 'Condition is: {}'.format(condition)
            raise ScorePriceError(t)

    @contextlib.contextmanager
    def filter_warnings(self):
        filterwarnings('ignore', category=RRuntimeWarning)
        yield
        resetwarnings()


class Score(ScorePriceBase):
    def __init__(self, app) -> None:
        super().__init__(app)
        with self.filter_warnings():
            r('scoreConfig <- Rdevicescore::models')
            r('scoreSchema <- Rdevicescore::schemas')
            # This is the function we call
            self.compute_score = r("""
                    function (input){
                        return (Rdevicescore::deviceScoreMain(input)) 
                    }""")
            self.validator = self.app.validator(condition_schema)

    def compute(self, device_id: str, condition: dict) -> dict:
        data = super().compute(device_id, condition)
        param = ListVector({
            'sourceData': data,
            'config': r.scoreConfig,
            'schema': r.scoreSchema,
            'versionSchema': '1.0',
            'versionScore': '1.0',
            'bUpgrade': False,
            'versionEntity': 'ereuse.org'
        })
        result, status, status_description = tuple(self.compute_score(param))
        status = int(status[0])
        if status != 0:
            message = '{} couldn\'t be computed for device {}, status {}'.format(self.__class__.__name__, device_id,
                                                                                 status_description)
            raise ScorePriceError(message)

        result = self._parse_response(result)
        FIELDS = 'Score', 'Ram.score', 'Processor.score', 'Drive.score', 'appearance.score', 'functionality.score'
        score, ram_score, processor_score, drive_score, appearance_score, functionality_score = list(
            map(lambda x: None if result[x] is NA_Real else round(result[x], self.ROUND_DECIMALS), FIELDS)
        )
        condition['general'] = {
            'score': score,
            'range': result['Range'],
        }
        condition['scoringSoftware'] = {
            'label': 'ereuse.org',
            'version': '1.0'
        }
        condition['components'] = {
            'ram': ram_score,
            'processors': processor_score,
            'hardDrives': drive_score
        }
        condition.setdefault('appearance', {})['score'] = appearance_score
        condition.setdefault('functionality', {})['score'] = functionality_score
        # Validate that the returned data complies with the schema
        self._validate(self.validator, condition, device_id)
        return condition


class Price(ScorePriceBase):
    def __init__(self, app) -> None:
        super().__init__(app)
        with self.filter_warnings():
            r('priceConfig <- Rdeviceprice::config')
            r('priceSchema <- Rdeviceprice::schemas')
            # This is the function we call
            self.compute_price = r("""
                function (input){
                    return (Rdeviceprice::devicePriceMain(input))
                }""")
            self.validator = self.app.validator(pricing)

    FIELDS = ('per', 'amount'), ('standard', '2yearsGuarantee'), ('refurbisher', 'retailer', 'platform')
    VAL = {'per': 'percentage', 'amount': 'amount'}
    SERVICE = {'2yearsGuarantee': 'guarantee', 'standard': 'standard'}

    def compute(self, device_id: str, condition: dict):
        data = super().compute(device_id, condition)
        param = ListVector({
            'sourceData': data,
            'config': r.priceConfig,
            'schema': r.priceSchema,
            'versionSchema': '1.0',
            'versionPrice': '1.0'
        })
        result = self._parse_response(self.compute_price(param))
        # Combinatronics of self.FIELDS to do d['refurbisher']['standard']['per'] = val['per.standard.refurbisher']
        d = defaultdict(lambda: defaultdict(dict))
        for val, service, role in itertools.product(*self.FIELDS):
            x = result['{}.{}.{}'.format(val, service, role)]
            if x is not NA_Real:
                d[role][self.SERVICE[service]][self.VAL[val]] = float(x)
        d['price'] = float(result['Price'])
        self._validate(self.validator, d, device_id)
        return d


class ScorePriceError(StandardError):
    pass


class ScorePriceNotSuitableError(StandardError):
    pass
