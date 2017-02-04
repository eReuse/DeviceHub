from ereuse_devicehub.resources.device.benchmark_settings import BenchmarkProcessor
from ereuse_devicehub.resources.device.component.settings import Component, ComponentSubSettings
from ereuse_devicehub.resources.schema import UnitCodes


class Processor(Component):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.numberOfCores = {
            'type': 'integer',
            'min': 1,
            'sink': 1
        }
        self.speed = {
            'type': 'float',
            'unitCode': UnitCodes.ghz,
            'sink': 1
        }
        self.address = {
            'type': 'integer',
            'unitCode': UnitCodes.bit,
            'allowed': {8, 16, 32, 64, 128, 256},
            'sink': -1
        }
        self.benchmark = {
            'type': 'dict',
            'schema': self.__proxy.generate_config_schema(BenchmarkProcessor),
            'writeonly': True,
        }
        self.benchmarks = {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': self.__proxy.generate_config_schema(BenchmarkProcessor)
            },
            'readonly': True
        }


class ProcessorSettings(ComponentSubSettings):
    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.schema = Processor
