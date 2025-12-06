import math
from collections import deque
from typing import TextIO, Iterable, cast
from common.file_solver import FileSolver
from common.grid import Grid

MathProblemType = tuple[str, Iterable[int]]

def load_pt1(file: TextIO) -> list[MathProblemType]:
    lines = file.readlines()
    operators, number_lines = lines[-1], lines[:-1]
    number_grid: list[list[int]] = [
        [int(n) for n in row.strip().split()]
        for row in number_lines
    ]
    transposed = zip(*number_grid)
    return list(zip(operators.split(), transposed))

def _solve_individual_problem(problem: MathProblemType) -> int:
    op, nums = problem
    return sum(nums) if op == '+' else math.prod(nums)

def load_pt2(file: TextIO) -> list[MathProblemType]:
    lines = file.readlines()

    max_line_length = max(len(l) for l in lines)

    operators, numbers = lines[-1], lines[:-1]
    data = deque()

    for col_idx in range(max_line_length):
        op = operators[col_idx] if col_idx < len(operators) else None
        if op in ('+', '*'):
            data.append((op, deque()))

        num = 0
        for row in numbers:
            if col_idx < len(row) and row[col_idx].isdigit():
                num = num * 10 + int(row[col_idx])
        if num:
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
