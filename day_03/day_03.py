import math
from collections import deque
from operator import itemgetter

from common.streaming_solver import StreamingSolver, create_summing_solution


LineDataType = list[int]


def parse_item(item_str: str) -> LineDataType:
    return [int(digit) for digit in item_str.strip()]


def part_one(data: LineDataType) -> int:
    return _get_largest_joltage_from_bank(data, 2)

def part_two(data: LineDataType) -> int:
    return _get_largest_joltage_from_bank(data, 12)

def _get_largest_joltage_from_bank(bank: list[int], num_batteries_to_use: int) -> int:
    q = deque()
    for i, bank_value in enumerate(bank):
        num_digits_left_in_bank = len(bank) - i
        while q and q[-1] < bank_value and (len(q) + num_digits_left_in_bank) > num_batteries_to_use:
            q.pop()

        q.append(bank_value)

    if len(q) < num_batteries_to_use:
        raise ValueError('No more banks to use')

    result = 0
    for _ in range(num_batteries_to_use):
        result = result * 10 + q.popleft()
    return result

if __name__ == "__main__":
    StreamingSolver[LineDataType, None].construct_for_day(
        day_number=3,
        item_parser=parse_item,
        solutions=[
            create_summing_solution(part_one),
            create_summing_solution(part_two),
        ]
    ).solve_all()
