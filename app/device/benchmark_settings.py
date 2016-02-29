import copy

from app.schema import UnitCodes, rdfs


class Benchmark:
    BENCHMARK_HARD_DRIVE = 'BenchmarkHardDrive'
    BENCHMARK_PROCESSOR = 'BenchmarkProcessor'
    TYPES = (
        BENCHMARK_HARD_DRIVE,
        BENCHMARK_PROCESSOR
    )

benchmark = copy.deepcopy(rdfs)

benchmark_hard_drive = copy.deepcopy(benchmark)
benchmark_hard_drive.update({
    'readingSpeed': {
        'type': 'float',
        'unitCode': UnitCodes.mbyte
    },
    'writingSpeed': {
        'type': 'float',
        'unitCode': UnitCodes.mbyte
    }
})
benchmark_hard_drive['@type']['allowed'] = Benchmark.BENCHMARK_HARD_DRIVE

benchmark_with_score = copy.deepcopy(benchmark)
benchmark_with_score.update({
    'score': {
        'type': 'float'
    }
})

benchmark_processor = copy.deepcopy(benchmark_with_score)
benchmark_processor['@type']['allowed'] = Benchmark.BENCHMARK_PROCESSOR


union_of_benchmarks = copy.deepcopy(dict(benchmark_hard_drive, **benchmark_processor))
union_of_benchmarks['@type']['allowed'] = Benchmark.TYPES
