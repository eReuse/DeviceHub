from ereuse_devicehub.resources.schema import UnitCodes, RDFS


class Benchmark(RDFS):
    BENCHMARK_HARD_DRIVE = 'BenchmarkHardDrive'
    BENCHMARK_PROCESSOR = 'BenchmarkProcessor'
    TYPES = (
        BENCHMARK_HARD_DRIVE,
        BENCHMARK_PROCESSOR
    )

    # noinspection PyAttributeOutsideInit
    def config(self, parent=None):
        self.readingSpeed = {
            'type': 'float',
            'unitCode': UnitCodes.mbyte
        }
        self.writingSpeed = {
            'type': 'float',
            'unitCode': UnitCodes.mbyte
        }


class BenchmarkHardDrive(Benchmark):
    pass


class BenchmarkWithScore(Benchmark):
    def config(self, parent=None):
        self.score = {
            'type': 'float'
        }


class BenchmarkProcessor(BenchmarkWithScore):
    pass
