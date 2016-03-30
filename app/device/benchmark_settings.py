from app.schema import UnitCodes, RDFS


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
    def _clean(cls, new_dict):
        full_dict = super(Benchmark, cls)._clean(new_dict)
        for val_name in ('BENCHMARK_HARD_DRIVE', 'BENCHMARK_PROCESSOR', 'TYPES'):
            if val_name in full_dict:
                del full_dict[val_name]
        return full_dict


class BenchmarkHardDrive(Benchmark):
    pass


class BenchmarkWithScore(Benchmark):
    score = {
        'type': 'float'
    }


class BenchmarkProcessor(BenchmarkWithScore):
    pass

