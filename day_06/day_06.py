import enum
import itertools
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

def load_pt2(file: TextIO) -> list[MathProblemType]:
    lines = file.readlines()
    transposed_lines = itertools.zip_longest(*lines, fillvalue='')

    data = deque()
    for line in transposed_lines:
        *digits, op = line
        if op in Operator:
            data.append((Operator(op), deque()))
        _, nums = data[-1]
        num_str = ''.join(digits).strip()
        if num_str:
            nums.append(int(num_str))

    return list(data)


def solve_problems(data: list[MathProblemType]) -> int:
    return sum(
        _solve_individual_problem(problem)
        for problem in data
    )


def _solve_individual_problem(problem: MathProblemType) -> int:
    op, nums = problem
    return sum(nums) if op == Operator.ADD else math.prod(nums)


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