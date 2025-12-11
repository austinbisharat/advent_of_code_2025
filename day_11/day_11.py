import dataclasses
from functools import lru_cache
from typing import TextIO, Iterable
from common.file_solver import FileSolver

LoadedDataType = dict[str, Iterable[str]]


def load(file: TextIO) -> LoadedDataType:
    def _parse_line(line: str) -> tuple[str, Iterable[str]]:
        inp, outs = line.strip().split(':')
        return inp, outs.strip().split()

    return dict(
        _parse_line(line)
        for line in file
    )


def solve_pt1(data: LoadedDataType) -> int:
    @lru_cache
    def _count_paths_to_end(cur: str) -> int:
        if cur == 'out':
            return 1

        if cur not in data:
            return 0

        res = sum(
            _count_paths_to_end(neighbor)
            for neighbor in data[cur]
        )
        return res

    return _count_paths_to_end('you')


@dataclasses.dataclass
class _PathData:
    total_paths: int
    paths_with_dac: int
    paths_with_fft: int
    paths_with_fft_and_dac: int

    def __iadd__(self, other: '_PathData') -> '_PathData':
        self.total_paths += other.total_paths
        self.paths_with_dac += other.paths_with_dac
        self.paths_with_fft += other.paths_with_fft
        self.paths_with_fft_and_dac += other.paths_with_fft_and_dac
        return self


def solve_pt2(data: LoadedDataType) -> int:
    @lru_cache
    def _count_paths_to_end(
        cur: str,
    ) -> _PathData:
        if cur == 'out':
            return _PathData(1, 0, 0, 0)

        if cur not in data:
            return _PathData(1, 0, 0, 0)

        res = _PathData(0, 0, 0, 0)

        for neighbor in data[cur]:
            neghbor_res = _count_paths_to_end(neighbor)
            res += neghbor_res

        if cur == 'dac':
            res.paths_with_dac = res.total_paths
            res.paths_with_fft_and_dac = max(res.paths_with_fft_and_dac, res.paths_with_fft)
        elif cur == 'fft':
            res.paths_with_fft = res.total_paths
            res.paths_with_fft_and_dac = max(res.paths_with_fft_and_dac, res.paths_with_dac)

        return res

    return _count_paths_to_end('svr').paths_with_fft_and_dac


if __name__ == "__main__":
    FileSolver[LoadedDataType].construct_for_day(
        day_number=11,
        loader=load,
        solutions=[solve_pt1, solve_pt2]
    ).solve_all()
