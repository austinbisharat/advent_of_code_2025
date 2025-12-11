import dataclasses
import itertools
import math
import sys
from collections import defaultdict

from common.streaming_solver import StreamingSolver, create_summing_solution

import pulp as pl


@dataclasses.dataclass
class MachineData:
    bitwise_indicator_lights: int
    buttons: list[list[int]]
    joltage_requirements: list[int]


def parse_item(item_str: str) -> MachineData:
    item_str = item_str.strip()
    indicator_lights, item_str = item_str.split(']')
    buttons, item_str = item_str.split('{')
    return MachineData(
        bitwise_indicator_lights=_parse_indicator_lights(indicator_lights[1:]),
        buttons = [
            [int(b) for b in button[1:-1].split(',')]
            for button in buttons.split()
        ],
        joltage_requirements=[
            int(c)
            for c in item_str[:-1].split(',')
        ]
    )

def _parse_indicator_lights(indicator: str) -> int:
    return sum(
        1 << i
        for i, char in enumerate(indicator)
        if char == '#'
    )

def part_one(data: MachineData) -> int:
    bitwise_buttons = [
        sum(1 << b for b in button)
        for button in data.buttons
    ]

    def _count_minimal_button_presses(current_lights: int, buttons: list[int]) -> int:
        if current_lights == 0:
            return 0
        elif len(buttons) == 0:
            return sys.maxsize

        return min(
            _count_minimal_button_presses(current_lights ^ buttons[0], buttons[1:]) + 1,
            _count_minimal_button_presses(current_lights, buttons[1:]),
        )

    res = _count_minimal_button_presses(data.bitwise_indicator_lights, bitwise_buttons)
    return res


def part_two(data: MachineData) -> int:
    memo: dict[tuple[int, ...], int] = defaultdict(lambda: sys.maxsize)

    def _count_minimal_button_presses(current_joltage_requirements: tuple[int, ...]) -> int:
        if all(j == 0 for j in current_joltage_requirements):
            return 0

        if any(j < 0 for j in current_joltage_requirements):
            return sys.maxsize

        if current_joltage_requirements in memo:
            return memo[current_joltage_requirements]

        res = min((
            1 + _count_minimal_button_presses(_press_button(current_joltage_requirements, b))
            for b in data.buttons
        ))
        memo[current_joltage_requirements] = res
        return res

    scale = math.gcd(*data.joltage_requirements)
    joltage_requirements = tuple(j // scale for j in data.joltage_requirements)
    res = _count_minimal_button_presses(joltage_requirements) * scale
    print(res)
    return res


def _press_button(current_joltage: tuple[int, ...], button: list[int], times: int = 1) -> tuple[int, ...]:
    cpy = list(current_joltage)
    for b in button:
        cpy[b] -= times
    return tuple(cpy)

def part_two_pl(data: MachineData) -> int:
    problem = pl.LpProblem('machine_data', pl.LpMinimize)
    pl_vars =[
        pl.LpVariable(f'button_{i}_{button}', lowBound=0, cat=pl.LpInteger)
        for i, button in enumerate(data.buttons)
    ]
    problem += pl.lpSum(pl_vars)
    for i, joltage_requirement in enumerate(data.joltage_requirements):
        sums_of_button_presses_for_joltage = pl.lpSum(
            pl_vars[j]
            for j, button in enumerate(data.buttons)
            if i in button
        )
        problem += sums_of_button_presses_for_joltage == joltage_requirement

    status = problem.solve(pl.PULP_CBC_CMD(msg=0))
    if status != 1:
        raise Exception('No solution')
    return int(pl.value(problem.objective))

if __name__ == "__main__":
    StreamingSolver[MachineData, None].construct_for_day(
        day_number=10,
        item_parser=parse_item,
        solutions=[
            create_summing_solution(part_one),
            create_summing_solution(part_two_pl)
        ]
    ).solve_all()
