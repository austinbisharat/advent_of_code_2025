import math
from typing import TextIO, cast

from common.file_solver import FileSolver


LoadedDataType = list[tuple[int, int]]


def load(file: TextIO) -> LoadedDataType:
    return [
        cast(tuple[int, int], tuple(map(int, range_str.strip().split("-"))))
        for range_str in file.read().strip().split(',')
    ]


def solve_pt1(data: LoadedDataType) -> int:
    # Assumes the ranges do not overlap
    return sum(
        _sum_simple_invalid_ids_in_range(id_range)
        for id_range in data
    )


def solve_pt2(data: LoadedDataType) -> int:
    return sum(
        _sum_complex_invalid_ids_in_range(id_range)
        for id_range in data
    )


def _sum_simple_invalid_ids_in_range(id_range: tuple[int, int]) -> int:
    lo, hi = id_range
    lo_digits, hi_digits = int(math.log10(lo)) + 1, int(math.log10(hi)) + 1
    return sum(
        _sum_invalid_ids_for_num_digits_and_repetitions(id_range, num_digits, 2)
        for num_digits in range(lo_digits, hi_digits + 1)
    )


def _sum_complex_invalid_ids_in_range(id_range: tuple[int, int]) -> int:
    lo, hi = id_range
    lo_digits, hi_digits = int(math.log10(lo)) + 1, int(math.log10(hi)) + 1
    return sum(
        _sum_complex_invalid_ids_in_range_for_num_digits(id_range, num_digits)
        for num_digits in range(lo_digits, hi_digits + 1)
    )


def _sum_complex_invalid_ids_in_range_for_num_digits(id_range: tuple[int, int], num_digits: int) -> int:
    sums_by_repetition_length = dict()
    total = 0
    for rep_len in range(1, num_digits//2 + 1):
        if num_digits % rep_len != 0:
            continue
        cur_sum = _sum_invalid_ids_for_num_digits_and_repetitions(id_range, num_digits, num_digits // rep_len)
        total += cur_sum
        for prev_rep_len, value in sums_by_repetition_length.items():
            if rep_len % prev_rep_len != 0:
                continue
            total -= value
        sums_by_repetition_length[rep_len] = cur_sum
    return total


def _sum_invalid_ids_for_num_digits_and_repetitions(id_range: tuple[int, int], num_digits: int, num_repetitions: int) -> int:
    lo, hi = id_range
    if num_digits % num_repetitions != 0:
        return 0

    incrementor = sum(
        10 ** (num_digits // num_repetitions * i)
        for i in range(num_repetitions)
    )
    lo_val_for_digit_range = max(lo, 10 ** (num_digits - 1))
    start = ((lo_val_for_digit_range + incrementor - 1) // incrementor) * incrementor
    end = (min(hi, 10 ** num_digits)) // incrementor * incrementor
    if start > end:
        return 0
    return (start + end) * ((end - start) // incrementor + 1) // 2


if __name__ == "__main__":
    FileSolver[LoadedDataType].construct_for_day(
        day_number=2,
        loader=load,
        solutions=[solve_pt1, solve_pt2]
    ).solve_all()
