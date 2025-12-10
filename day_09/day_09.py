import itertools
from typing import TextIO, cast
from common.file_solver import FileSolver

import shape

LoadedDataType = list[tuple[int, int]]


def load(file: TextIO) -> LoadedDataType:
    return [
        cast(tuple[int, int], tuple(map(int, reversed(line.strip().split(',')))))
        for line in file
    ]

def _area(top_corner: tuple[int, int], bot_corner: tuple[int, int]):
    top_row, top_col = top_corner
    bot_row, bot_col = bot_corner
    return (abs(top_row - bot_row) + 1) * (abs(top_col - bot_col) + 1)

def solve_pt1(points: LoadedDataType) -> int:
    return max(
        _area(l, r)
        for l, r in itertools.combinations(points, 2)
    )

def solve_pt2(points: LoadedDataType) -> int:
    return max(area for area in shape.get_areas_for_possible_rects(points))


if __name__ == "__main__":
    FileSolver[LoadedDataType].construct_for_day(
        day_number=9,
        loader=load,
        solutions=[
            solve_pt1,
            solve_pt2,
        ]
    ).solve_all()
