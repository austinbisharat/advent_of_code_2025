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
    return sum(
        _sum_invalid_ids_for_num_digits_and_repetitions(id_range, num_digits, 2)
        for id_range in data
        for num_digits in _get_num_digits_to_consider_for_id_range(id_range)
        if num_digits % 2 == 0
    )


def solve_pt2(data: LoadedDataType) -> int:
    # Assumes the given ranges do not overlap
    return sum(
        _sum_complex_invalid_ids_in_range_for_num_digits(id_range, num_digits)
        for id_range in data
        for num_digits in _get_num_digits_to_consider_for_id_range(id_range)
    )

def _get_num_digits_to_consider_for_id_range(id_range: tuple[int, int]) -> Iterable[int]:
    lo_digit_count, hi_digit_count = map(lambda x: int(math.log10(x)) + 1, id_range)
    return range(lo_digit_count, hi_digit_count + 1)


def _sum_complex_invalid_ids_in_range_for_num_digits(id_range: tuple[int, int], num_digits: int) -> int:
    sums_by_repetition_length = dict()
    total = 0
    for repetition_len in range(1, num_digits//2 + 1):
        if num_digits % repetition_len != 0:
            continue

        cur_sum = _sum_invalid_ids_for_num_digits_and_repetitions(id_range, num_digits, num_digits // repetition_len)
        total += cur_sum

        for prev_repetition_len, value in sums_by_repetition_length.items():
            # If the current repetition length is a logical superset of a previous repetition length,
            # we need to remove the prev repetition length's sum from our total sum. Notably, this
            # might happen multiple times. For example, when num_digits = 10, we will subtract the
            # value for repetition_len == 1 twice, since that set of invalid ids will be logically
            # contained by the sets of invalid ids with repetition_len 2 AND 5
            if repetition_len % prev_repetition_len == 0:
                total -= value
        sums_by_repetition_length[repetition_len] = cur_sum
    return total


def _sum_invalid_ids_for_num_digits_and_repetitions(id_range: tuple[int, int], num_digits: int, num_repetitions: int) -> int:
    lo, hi = id_range

    # All invalid IDs of the given repetition length will be divisible by this step value. Some examples:
    # - num_digits = 2, num_repetitions = 2 -> step should be 11
    # - num_digits = 4, num_repetitions = 2 -> step should be 1010
    # - num_digits = 6, num_repetitions = 2 -> step should be 100100
    # - num_digits = 6, num_repetitions = 3 -> step should be 101010
    step = sum(
        10 ** (num_digits // num_repetitions * i)
        for i in range(num_repetitions)
    )

    # Get the min and max of the range for the current number of digits we're considering
    min_id_for_num_digits = max(lo, 10 ** (num_digits - 1))
    max_id_for_num_digits = min(hi, 10 ** num_digits)

    # Round UP to the next multiple of step to get the first invalid id
    min_invalid_id = (min_id_for_num_digits + step - 1) // step * step

    # Round DOWN to the next multiple of step to get the last invalid id
    max_invalid_id = max_id_for_num_digits // step * step

    return _sum_arithmetic_sequence(min_invalid_id, max_invalid_id, step)

def _sum_arithmetic_sequence(start: int, end: int, step: int) -> int:
    """
    Sums arithmetic sequence

    Start and end are inclusive. Assumes end-start is divisible by step.
    """
    num_elements = (end - start) // step + 1
    return (start + end) *  num_elements // 2


if __name__ == "__main__":
    FileSolver[LoadedDataType].construct_for_day(
        day_number=2,
        loader=load,
        solutions=[solve_pt1, solve_pt2]
    ).solve_all()
