import dataclasses
import heapq
import itertools
import math
import sys
from collections import defaultdict
from functools import lru_cache

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


@dataclasses.dataclass(order=True)
class _SearchNode:
    presses_so_far: int
    neg_gcd: int
    joltage_requirements: tuple[int, ...]


def _find_nearest_divisible_joltage_req(
    current_joltage_requirements: tuple[int, ...],
    machine: MachineData,
) -> _SearchNode:
    heap = [_SearchNode(
        presses_so_far=0,
        neg_gcd=-1 * math.gcd(*current_joltage_requirements),
        joltage_requirements=current_joltage_requirements
    )]

    while heap:
        node = heapq.heappop(heap)
        if node.neg_gcd < -1 or all(j == 0 for j in node.joltage_requirements):
            return node

        for b in machine.buttons:
            next_joltage_requirements = _press_button(node.joltage_requirements, b)
            if any(j < 0 for j in next_joltage_requirements):
                continue
            heapq.heappush(heap, _SearchNode(
                presses_so_far=node.presses_so_far + 1,
                neg_gcd=-1 * math.gcd(*next_joltage_requirements),
                joltage_requirements=next_joltage_requirements
            ))

    raise ValueError('Should never happen')


def part_two(data: MachineData) -> int:
    @lru_cache
    def _count_minimal_button_presses(current_joltage_requirements: tuple[int, ...]) -> int:
        if any(j < 0 for j in current_joltage_requirements):
            return sys.maxsize

        node = _find_nearest_divisible_joltage_req(current_joltage_requirements, data)
        if all(j == 0 for j in node.joltage_requirements):
            return node.presses_so_far

        scale = -1 * node.neg_gcd
        current_joltage_requirements = tuple(j // scale for j in node.joltage_requirements)
        return node.presses_so_far + scale * _count_minimal_button_presses(current_joltage_requirements)

    try:
        res = _count_minimal_button_presses(tuple(data.joltage_requirements))
    except ValueError:
        res = -1
    print(f'cs: {res}')
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

    res = int(pl.value(problem.objective))
    print(f'pl: {res}\n')
    return res

if __name__ == "__main__":
    StreamingSolver[MachineData, None].construct_for_day(
        day_number=10,
        item_parser=parse_item,
        solutions=[
            create_summing_solution(part_one),
            create_summing_solution(part_two),
            create_summing_solution(part_two_pl)
        ]
    ).solve_all()
