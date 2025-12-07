from collections import defaultdict
from typing import TextIO

from common.streaming_solver import StreamingSolver, AbstractItemStreamingSolution


START_LOC = 'S'
SPLIT_LOC = '^'


def load_start_location(file: TextIO) -> int:
    return file.readline().find(START_LOC)


class Part1Solution(AbstractItemStreamingSolution[str, int]):
    def __init__(self) -> None:
        self._split_count = 0
        self._active_columns: set[int] = set()

    def load_config(self, start_loc: int) -> None:
        self._active_columns.add(start_loc)

    def process_item(self, line: str) -> None:
        new_cols = self._active_columns.copy()
        for col in self._active_columns:
            if line[col] != SPLIT_LOC:
                continue

            self._split_count += 1
            new_cols.remove(col)
            if col-1 >= 0:
                new_cols.add(col-1)
            if col+1 < len(line):
                new_cols.add(col+1)

        self._active_columns = new_cols

    def result(self) -> int:
        return self._split_count


class Part2Solution(AbstractItemStreamingSolution[str, int]):
    def __init__(self) -> None:
        self._split_count = 0
        self._active_column_to_timeline_count: dict[int, int] = defaultdict(int)

    def load_config(self, start_loc: int) -> None:
        self._active_column_to_timeline_count[start_loc] += 1

    def process_item(self, line: str) -> None:
        new_cols = defaultdict(int)
        for col in self._active_column_to_timeline_count:
            if line[col] != SPLIT_LOC:
                new_cols[col] += self._active_column_to_timeline_count[col]
                continue

            self._split_count += 1
            if col-1 >= 0:
                new_cols[col-1] += self._active_column_to_timeline_count[col]
            if col+1 < len(line):
                new_cols[col+1] += self._active_column_to_timeline_count[col]

        self._active_column_to_timeline_count = new_cols

    def result(self) -> int:
        return sum(self._active_column_to_timeline_count.values())


if __name__ == "__main__":
    StreamingSolver[str, int].construct_for_day(
        file_config_parser=load_start_location,
        day_number=7,
        item_parser=lambda line: line,
        solutions=[Part1Solution, Part2Solution]
    ).solve_all()
