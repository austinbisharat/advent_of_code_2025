from typing import TextIO

from common.streaming_solver import StreamingSolver, create_summing_solution, create_summing_solution_with_file_config

LineDataType = tuple[tuple[int, int], list[int]]
ShapeConfig = list[int]

def parse_shape_config(file: TextIO) -> ShapeConfig:
    shapes = []

    cur_shape_size = 0
    for line in file:
        if line[0] == '-':
            shapes.append(cur_shape_size)
            return shapes

        if not line.strip():
            shapes.append(cur_shape_size)
            cur_shape_size = 0
            continue

        if line.strip()[0] == ':':
            continue

        cur_shape_size += sum(1 for c in line.strip() if c == '#')


def parse_item(item_str: str) -> LineDataType:
    grid_shape, shape_counts = item_str.strip().split(': ')
    rows, cols = [int(val) for val in grid_shape.split('x')]
    shape_counts = [int(val) for val in shape_counts.split()]
    return (rows, cols), shape_counts


def part_one(row_data: LineDataType, shape_sizes: ShapeConfig) -> int:
    (rows, cols), shape_counts = row_data
    if (rows // 3 * cols // 3) >= sum(shape_counts):
        return 1

    total_space = sum(shape_count * shape_size for shape_count, shape_size in zip(shape_counts, shape_sizes))
    if total_space > rows * cols:
        return 0

    print(row_data)
    raise NotImplementedError('Check this case')


if __name__ == "__main__":
    StreamingSolver[LineDataType, ShapeConfig].construct_for_day(
        day_number=12,
        file_config_parser=parse_shape_config,
        item_parser=parse_item,
        solutions=[
            create_summing_solution_with_file_config(part_one)
        ]
    ).solve_file('input_12.txt')
