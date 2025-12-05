import bisect
import itertools
from collections import deque
from typing import TextIO, Iterable

from common.streaming_solver import StreamingSolver, AbstractItemStreamingSolution

FileConfigType = list[tuple[int, int]]
LineDataType = int

def load_config(file: TextIO) -> FileConfigType:
    q = deque()

    for line in file:
        if not line.strip():
            return list(q)
        q.append(tuple(map(int, line.strip().split("-"))))
    return list(q)

def parse_item(item_str: str) -> LineDataType:
    return int(item_str.strip())


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

class Part1Solution(AbstractItemStreamingSolution[LineDataType, FileConfigType]):
    def __init__(self) -> None:
        self._count = 0
        self._flattened_ranges = []

    def load_config(self, config: FileConfigType) -> None:
        self._flattened_ranges = list(itertools.chain.from_iterable(_combine_ranges(config)))

    def process_item(self, item: LineDataType) -> None:
        idx = bisect.bisect_left(self._flattened_ranges, item)
        if idx < len(self._flattened_ranges) and (self._flattened_ranges[idx] == item or idx % 2 == 1):
            self._count += 1

    def result(self) -> int:
        return self._count


class Part2Solution(AbstractItemStreamingSolution[LineDataType, FileConfigType]):
    def __init__(self) -> None:
        self._count = 0
        self._config = []

    # TODO: a bit clunky to use load_config for this. Should separate out part 2 to a different type of solver
    def load_config(self, config: FileConfigType) -> None:
        for lo, hi in _combine_ranges(config):
            self._count += hi - lo + 1

    def process_item(self, item: LineDataType) -> None:
        ...

    def result(self) -> int:
        return self._count


if __name__ == "__main__":
    StreamingSolver[LineDataType, FileConfigType].construct_for_day(
        day_number=5,
        file_config_parser=load_config,
        item_parser=parse_item,
        solutions=[Part1Solution, Part2Solution]
    ).solve_all()
