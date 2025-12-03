from common.streaming_solver import StreamingSolver, create_summing_solution


LineDataType = list[int]


def parse_item(item_str: str) -> LineDataType:
    return [int(digit) for digit in item_str.strip()]


def part_one(data: LineDataType) -> int:
    return _get_largest_joltage_from_bank(data, 2)

def part_two(data: LineDataType) -> int:
    return _get_largest_joltage_from_bank(data, 12)

def _get_largest_joltage_from_bank(bank: LineDataType, num_remaining_digits: int, result_so_far: int = 0) -> int:
    if num_remaining_digits == 0:
        return result_so_far
    num_remaining_digits -= 1
    possible_next_digits = bank[:len(bank) - num_remaining_digits]
    first_digit_index, first_digit = max(enumerate(possible_next_digits), key=lambda pair: pair[1])
    result_so_far = result_so_far * 10 + first_digit
    return _get_largest_joltage_from_bank(bank[first_digit_index + 1:], num_remaining_digits, result_so_far)


if __name__ == "__main__":
    StreamingSolver[LineDataType, None].construct_for_day(
        day_number=3,
        item_parser=parse_item,
        solutions=[
            create_summing_solution(part_one),
            create_summing_solution(part_two)
        ]
    ).solve_all()
