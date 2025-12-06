import enum
import math
from collections import deque
from typing import TextIO, Iterable
from common.file_solver import FileSolver


class Operator(enum.Enum):
    ADD = '+'
    MUL = '*'

MathProblemType = tuple[Operator, Iterable[int]]


def load_pt1(file: TextIO) -> list[MathProblemType]:
    lines = file.readlines()
    operators, number_lines = lines[-1], lines[:-1]
    number_grid: list[list[int]] = [
        [int(n) for n in row.strip().split()]
        for row in number_lines
    ]
    transposed_nums = zip(*number_grid)
    ops = [Operator(op) for op in operators.split()]
    return list(zip(ops, transposed_nums))

def _solve_individual_problem(problem: MathProblemType) -> int:
    op, nums = problem
    return sum(nums) if op == Operator.ADD else math.prod(nums)

def load_pt2(file: TextIO) -> list[MathProblemType]:
    lines = file.readlines()

    max_line_length = max(len(l) for l in lines)

    operators, numbers = lines[-1], lines[:-1]
    data = deque()

    for col_idx in range(max_line_length):
        if (
            col_idx < len(operators)
            and operators[col_idx] in Operator
        ):
            data.append((Operator(operators[col_idx]), deque()))

        num = 0
        for row in numbers:
            if col_idx < len(row) and row[col_idx].isdigit():
                num = num * 10 + int(row[col_idx])

        if not num:
            continue

        if not data:
            raise Exception('Trying to add number to unknown operator')
        data[-1][1].append(num)

    return list(data)


def solve_problems(data: list[MathProblemType]) -> int:
    return sum(
        _solve_individual_problem(problem)
        for problem in data
    )


if __name__ == "__main__":
    FileSolver[list[MathProblemType]].construct_for_day(
        day_number=6,
        loader=load_pt1,
        solutions=[solve_problems]
    ).solve_all()

    FileSolver[list[MathProblemType]].construct_for_day(
        day_number=6,
        loader=load_pt2,
        solutions=[solve_problems]
    ).solve_all()
