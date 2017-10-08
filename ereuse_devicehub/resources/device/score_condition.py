import contextlib
import itertools
from collections import defaultdict
from warnings import filterwarnings, resetwarnings

from pydash import ceil
from rpy2.rinterface import NA_Real, RRuntimeWarning
from rpy2.robjects import DataFrame, ListVector, packages as rpackages, r

from ereuse_devicehub.exceptions import StandardError
from ereuse_devicehub.export.export import SpreadsheetTranslator
from ereuse_devicehub.resources.account.domain import AccountDomain
from ereuse_devicehub.resources.condition import condition as condition_schema
from ereuse_devicehub.resources.device.computer.settings import Computer
from ereuse_devicehub.resources.device.domain import DeviceDomain
from ereuse_devicehub.resources.pricing import pricing
from ereuse_devicehub.validation.validation import DeviceHubValidator


class ScorePriceBase:
    """
    Abstract class to compute device attributes, like score and pricing, that use R libraries for such purpose.

    The way of executing this class is as follows:

    1. Get a device with all the data needed by executing``get_device()``.
    2. Then execute ``compute()`` to generate the score/price.

    See an example in
    :py:func:`ereuse_devicehub.resources.event.device.snapshot.hooks.compute_condition_price_and_materialize_in_device`.
    """
    ROUND_DECIMALS = 2

    def __init__(self, app) -> None:
        self.app = app
        self.translator = SpreadsheetTranslator(brief=False)
        self.validator = NotImplementedError()
        self.library_kwargs = {'lib_loc': app.config['R_PACKAGES_PATH']} if app.config['R_PACKAGES_PATH'] else {}

    @staticmethod
    def get_device(device_id: str, condition: dict) -> dict:
        """
        Retrieves a device alongside its full components, part of their events and condition –everything needed
        for ``compute`` to get the score or the price.
        :return: The device.
        """
        # We can't compute empty conditions or anything that is not a computer
        if not condition:
            raise ScorePriceNotSuitableError()
        device = DeviceDomain.get_one(device_id)
        if device['@type'] != Computer.type_name:
            raise ScorePriceNotSuitableError()
        device['components'] = DeviceDomain.get_full_components(device['components'])
        device['condition'] = condition
        return device

    def compute(self, device: dict) -> DataFrame:
        """Computes the score or condition. Subclass this method to perform something valuable."""
        keys, values = self.translator.translate([device])
        # R cannot parse parenthesis in fieldnames
        data = {key.replace('(', '.').replace(')', '.'): val for key, val in zip(keys, values)}
        return DataFrame(data)

    @staticmethod
    def _parse_response(data: DataFrame) -> dict:
        """Parses the DataFrame returned from eReuse.org's R libraries to a dictionary."""
        return {name: data[i][0] for i, name in enumerate(data.names)}

    def _validate(self, validator: DeviceHubValidator, value: dict, device_id: str):
        """
        Validates the passed-in ``value`` against the validator ``validator``.
        :raise ScorePriceError: If validation is wrong.
        """
        if not validator.validate(value):
            t = '{} wrong condition or pricing:\n'.format(self.__class__.__name__)
            t += 'Device {} of {}\n'.format(device_id, AccountDomain.requested_database)
            t += 'Condition or pricing is: {}\n'.format(value)
            t += 'Validation error is: {}'.format(validator.errors)
            raise ScorePriceError(t)

    @contextlib.contextmanager
    def filter_warnings(self):
        """Filter warning coming from R. Use it in a ``with`` block."""
        filterwarnings('ignore', category=RRuntimeWarning)
        yield
        resetwarnings()


class Score(ScorePriceBase):
    """
    Computes the Score of a device.

    When calling ``compute``, this class sends the passed-in ``device`` to the Rdevicescore R package and returns
    the ``condition`` representing the score.
    """

    def __init__(self, app) -> None:
        super().__init__(app)
        with self.filter_warnings():
            r.library('Rdevicescore', **self.library_kwargs)
            self.compute_score = rpackages.importr('Rdevicescore').deviceScoreMain
            r('deviceScoreConfig <- Rdevicescore::models')
            r('deviceScoreSchema <- Rdevicescore::schemas')

        # This is the function we call
        self.validator = self.app.validator(condition_schema)

    def compute(self, device) -> dict:
        """Computes the score for the passed-in ``device``. This method mutates ``device.condition``."""
        data = super().compute(device)
        param = ListVector({
            'sourceData': data,
            'config': r.deviceScoreConfig,
            'schema': r.deviceScoreSchema,
            'versionSchema': '1.0',
            'versionScore': '1.0',
            'bUpgrade': False,
            'versionEntity': 'ereuse.org'
        })
        result, status, status_description = tuple(self.compute_score(param))
        status = int(status[0])
        if status != 0:
            message = '{} couldn\'t be computed for device {}, status {}'.format(self.__class__.__name__, device['_id'],
                                                                                 status_description)
            raise ScorePriceError(message)

        result = self._parse_response(result)
        FIELDS = 'Score', 'Ram.score', 'Processor.score', 'Drive.score', 'appearance.score', 'functionality.score'
        score, ram_score, processor_score, drive_score, appearance_score, functionality_score = list(
            map(lambda x: None if result[x] is NA_Real else round(result[x], self.ROUND_DECIMALS), FIELDS)
        )
        condition = device['condition']
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
        self._validate(self.validator, condition, device['_id'])
        return device['condition']


class Price(ScorePriceBase):
    """As Score, but computing the Price."""

    def __init__(self, app) -> None:
        super().__init__(app)
        with self.filter_warnings():
            r.library('Rdeviceprice', **self.library_kwargs)
            self.compute_price = rpackages.importr('Rdeviceprice').devicePriceMain
            r('devicePriceConfig <- Rdeviceprice::config')
            r('devicePriceSchemas <- Rdeviceprice::schemas')
        self.validator = self.app.validator(pricing)

    FIELDS = ('per', 'amount'), ('standard', '2yearsGuarantee'), ('refurbisher', 'retailer', 'platform')
    VAL = {'per': 'percentage', 'amount': 'amount'}
    SERVICE = {'2yearsGuarantee': 'guarantee', 'standard': 'standard'}

    def compute(self, device: dict):
        """Computes the price of the passed-in ``device``. This method mutates ``device.pricing``."""
        data = super().compute(device)
        param = ListVector({
            'sourceData': data,
            'config': r.devicePriceConfig,
            'schema': r.devicePriceSchemas,
            'versionSchema': '1.0',
            'versionPrice': '1.0'
        })
        result = self._parse_response(self.compute_price(param))
        # Combinatronics of self.FIELDS to do d['refurbisher']['standard']['per'] = val['per.standard.refurbisher']
        d = defaultdict(lambda: defaultdict(dict))
        for val, service, role in itertools.product(*self.FIELDS):
            x = result['{}.{}.{}'.format(val, service, role)]
            if x is not NA_Real:
                d[role][self.SERVICE[service]][self.VAL[val]] = round(x, self.ROUND_DECIMALS)
        # Let's remove some differences in rounding above by ceiling the final price
        d['total'] = ceil(result['Price'], self.ROUND_DECIMALS)
        self._validate(self.validator, d, device['_id'])
        device['pricing'] = d
        return d


class ScorePriceError(StandardError):
    pass


class ScorePriceNotSuitableError(StandardError):
    pass
