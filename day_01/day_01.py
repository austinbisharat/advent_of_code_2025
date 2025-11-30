from typing import TextIO
from common.file_solver import FileSolver


LoadedDataType = ...


def load(file: TextIO) -> LoadedDataType:
    ...


def solve_pt1(data: LoadedDataType) -> int:
    ...


def solve_pt2(data: LoadedDataType) -> int:
    return 0


if __name__ == "__main__":
    FileSolver[LoadedDataType].construct_for_day(
        day_number=1,
        loader=load,
        solutions=[solve_pt1, solve_pt2]
    ).solve_all()
