import itertools
import math
from collections import defaultdict
from typing import TextIO, cast
from common.file_solver import FileSolver
import heapq

JunctionPointType = tuple[int, int, int]
LoadedDataType = tuple[int, list[JunctionPointType]]


def load(file: TextIO) -> LoadedDataType:
    return int(file.readline().strip()), [
        cast(JunctionPointType, tuple(map(int, line.strip().split(','))))
        for line in file
    ]

def _compute_distance(l: JunctionPointType, r: JunctionPointType) -> float:
    return math.sqrt(sum((l_i - r_i) ** 2 for l_i, r_i in zip(l, r)))

def solve_pt1(data: LoadedDataType) -> int:
    num_connections, junctions = data
    heap = list()
    for l, r in itertools.combinations(junctions, 2):
        item = _compute_distance(l, r), l, r
        heapq.heappush(heap, item)

    junction_to_circuit = defaultdict(set)
    for _ in range(num_connections):
        dist, l, r = heapq.heappop(heap)
        new_circuit = junction_to_circuit[l].union(junction_to_circuit[r])
        new_circuit.add(l)
        new_circuit.add(r)
        for junction in new_circuit:
            junction_to_circuit[junction] = new_circuit

    circuit_lens = {id(circuit): len(circuit) for circuit in junction_to_circuit.values()}
    lens = sorted(circuit_lens.values(), reverse=True)
    return math.prod(lens[:3])

def solve_pt2(data: LoadedDataType) -> int:
    num_connections, junctions = data
    heap = list()
    for l, r in itertools.combinations(junctions, 2):
        item = _compute_distance(l, r), l, r
        heapq.heappush(heap, item)

    junction_to_circuit = defaultdict(set)
    while True:
        dist, l, r = heapq.heappop(heap)
        new_circuit = junction_to_circuit[l].union(junction_to_circuit[r])
        new_circuit.add(l)
        new_circuit.add(r)
        if len(new_circuit) == len(junctions):
            return l[0] * r[0]

        for junction in new_circuit:
            junction_to_circuit[junction] = new_circuit


if __name__ == "__main__":
    FileSolver[LoadedDataType].construct_for_day(
        day_number=8,
        loader=load,
        solutions=[solve_pt1, solve_pt2]
    ).solve_all()
