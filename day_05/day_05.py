import bisect
import itertools
from collections import deque
from typing import TextIO, Iterable, cast

from common.file_solver import FileSolver
from common.streaming_solver import StreamingSolver, AbstractItemStreamingSolution


def parse_ranges(file: TextIO) -> list[tuple[int, int]]:
    q = deque()
    for line in file:
        if not line.strip():
            return list(q)
        q.append(parse_range(line))
    return list(q)

def parse_id(item_str: str) -> int:
    return int(item_str.strip())

def parse_range(range_str: str) -> tuple[int, int]:
    return cast(tuple[int, int], tuple(map(int, range_str.strip().split("-"))))


def _combine_ranges(ranges: list[tuple[int, int]]) -> Iterable[tuple[int, int]]:
    (cur_lo, cur_hi), *ranges, (last_lo, last_hi) = sorted(ranges)
    for next_lo, next_hi in ranges:
        if cur_lo <= next_lo <= cur_hi:
            cur_hi = max(cur_hi, next_hi)
        else:
            yield cur_lo, cur_hi
            cur_lo, cur_hi = next_lo, next_hi

    if cur_lo <= last_lo <= cur_hi:
        yield cur_lo, max(cur_hi, last_hi)
    else:
        yield cur_lo, cur_hi
        yield last_lo, last_hi

class Part1Solution(AbstractItemStreamingSolution[int, list[tuple[int, int]]]):
    def __init__(self) -> None:
        self._count = 0
        self._flattened_ranges = []

    def load_config(self, config: list[tuple[int, int]]) -> None:
        self._flattened_ranges = list(itertools.chain.from_iterable(_combine_ranges(config)))

    def process_item(self, item: int) -> None:
        idx = bisect.bisect_left(self._flattened_ranges, item)
        if idx < len(self._flattened_ranges) and (self._flattened_ranges[idx] == item or idx % 2 == 1):
            self._count += 1

    def result(self) -> int:
        return self._count


def solve_pt2(ranges: list[tuple[int, int]]) -> int:
    return sum ((
        hi - lo + 1
        for lo, hi in _combine_ranges(ranges)
    ))


if __name__ == "__main__":
    StreamingSolver[int, list[tuple[int, int]]].construct_for_day(
        day_number=5,
        file_config_parser=parse_ranges,
        item_parser=parse_id,
        solutions=[Part1Solution]
    ).solve_all()

    FileSolver[list[tuple[int, int]]].construct_for_day(
        day_number=5,
        loader=parse_ranges,
        solutions=[solve_pt2],
    ).solve_all()

