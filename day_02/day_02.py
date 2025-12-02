import itertools
import math
from typing import TextIO, cast, Iterable

from common.file_solver import FileSolver


LoadedDataType = list[tuple[int, int]]


def load(file: TextIO) -> LoadedDataType:
    return [
        cast(tuple[int, int], tuple(map(int, range_str.strip().split("-"))))
        for range_str in file.read().strip().split(',')
    ]


def solve_pt1(data: LoadedDataType) -> int:
    # Assumes the ranges do not overlap
    return sum(set(itertools.chain.from_iterable(
        _generate_simple_invalid_ids_in_range(id_range)
        for id_range in data
    )))

def solve_pt2(data: LoadedDataType) -> int:
    return sum(set(itertools.chain.from_iterable(
        _generate_complex_invalid_ids_in_range(id_range)
        for id_range in data
    )))

def _generate_simple_invalid_ids_in_range(id_range: tuple[int, int]) -> Iterable[int]:
    lo, hi = id_range
    lo_digits, hi_digits = int(math.log10(lo)) + 1, int(math.log10(hi)) + 1
    for num_digits in range(lo_digits, hi_digits + 1):
        yield from _generate_invalid_ids_for_num_digits_and_repetitions(hi, lo, num_digits, 2)

def _generate_complex_invalid_ids_in_range(id_range: tuple[int, int]) -> Iterable[int]:
    lo, hi = id_range
    lo_digits, hi_digits = int(math.log10(lo)) + 1, int(math.log10(hi)) + 1
    for num_digits in range(lo_digits, hi_digits + 1):
        for num_repetitions in range(2, num_digits + 1):
            yield from _generate_invalid_ids_for_num_digits_and_repetitions(hi, lo, num_digits, num_repetitions)

def _generate_invalid_ids_for_num_digits_and_repetitions(hi, lo, num_digits, num_repetitions):
    if num_digits % num_repetitions != 0:
        return

    incrementor = sum(
        10 ** (num_digits // num_repetitions * i)
        for i in range(num_repetitions)
    )
    lo_val_for_digit_range = max(lo, 10 ** (num_digits - 1))
    start = ((lo_val_for_digit_range + incrementor - 1) // incrementor) * incrementor
    end = (min(hi, 10 ** num_digits)) // incrementor * incrementor
    yield from range(start, end + 1, incrementor)

if __name__ == "__main__":
    FileSolver[LoadedDataType].construct_for_day(
        day_number=2,
        loader=load,
        solutions=[solve_pt1, solve_pt2]
    ).solve_all()
