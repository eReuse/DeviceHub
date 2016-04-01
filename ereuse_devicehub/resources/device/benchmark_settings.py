from collections import Sequence

from ereuse_devicehub.resources.schema import UnitCodes, RDFS


class Benchmark(RDFS):
    BENCHMARK_HARD_DRIVE = 'BenchmarkHardDrive'
    BENCHMARK_PROCESSOR = 'BenchmarkProcessor'
    TYPES = (
        BENCHMARK_HARD_DRIVE,
        BENCHMARK_PROCESSOR
    )
    readingSpeed = {
        'type': 'float',
        'unitCode': UnitCodes.mbyte
    }
    writingSpeed = {
        'type': 'float',
        'unitCode': UnitCodes.mbyte
    }


    @classmethod
    def _clean(cls, attributes: dict, attributes_to_remove: tuple = None) -> dict:
        attributes_to_remove = tuple() if attributes_to_remove is None else attributes_to_remove
        benchmark_attributes_to_remove = ('BENCHMARK_HARD_DRIVE', 'BENCHMARK_PROCESSOR', 'TYPES')
        return super(Benchmark, cls)._clean(attributes, attributes_to_remove + benchmark_attributes_to_remove)


class BenchmarkHardDrive(Benchmark):
    pass


class BenchmarkWithScore(Benchmark):
    score = {
        'type': 'float'
    }


class BenchmarkProcessor(BenchmarkWithScore):
    pass

