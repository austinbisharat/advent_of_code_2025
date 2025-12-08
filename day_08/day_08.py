import itertools
import math
import time
from collections import defaultdict
from typing import TextIO, cast, Iterable

from common.file_solver import FileSolver
import heapq

JunctionPointType = tuple[int, int, int]
LoadedDataType = tuple[int, list[JunctionPointType]]

JunctionDistType = tuple[float, JunctionPointType, JunctionPointType]


def load(file: TextIO) -> LoadedDataType:
    return int(file.readline().strip()), [
        cast(JunctionPointType, tuple(map(int, line.strip().split(','))))
        for line in file
    ]


def _compute_distance(l: JunctionPointType, r: JunctionPointType) -> float:
    return sum((l_i - r_i) ** 2 for l_i, r_i in zip(l, r))


def _compute_closest_connections(junctions: list[JunctionPointType]) -> list[JunctionDistType]:
    heap = list()
    for l, r in itertools.combinations(junctions, 2):
        item = _compute_distance(l, r), l, r
        heapq.heappush(heap, item)
    return heap


class Circuits:
    def __init__(self, junctions: list[JunctionPointType]) -> None:
        self._junction_to_parent = {
            j: j for j in junctions
        }
        self._parent_to_size = {
            j: 1 for j in junctions
        }

    def merge(self, l: JunctionPointType, r: JunctionPointType) -> int:
        l_parent = self._find_parent(l)
        r_parent = self._find_parent(r)

        if l_parent == r_parent:
            return self._parent_to_size[r_parent]

        if self._parent_to_size[l_parent] > self._parent_to_size[r_parent]:
            l_parent, r_parent = r_parent, l_parent

        self._junction_to_parent[l_parent] = r_parent
        self._find_parent(l_parent)
        self._parent_to_size[r_parent] += self._parent_to_size[l_parent]
        return self._parent_to_size[r_parent]

    def _find_parent(self, junction: JunctionPointType) -> JunctionPointType:
        cur = junction
        while self._junction_to_parent[cur] != cur:
            cur = self._junction_to_parent[cur]

        root = cur
        cur = junction
        while self._junction_to_parent[cur] != root:
            parent = self._junction_to_parent[cur]
            self._junction_to_parent[cur] = root
            cur = parent
        return root

    def get_top_n_largest_sets(self, n: int) -> Iterable[int]:
        parents = set(self._junction_to_parent.values())
        heap = [self._parent_to_size[p] for p in parents]
        heapq.heapify(heap)
        return heapq.nlargest(n, heap)


def solve_pt1(data: LoadedDataType) -> int:
    num_connections, junctions = data
    heap = _compute_closest_connections(junctions)

    circuits = Circuits(junctions)
    for dist, l, r in heapq.nsmallest(num_connections, heap):
        circuits.merge(l, r)
    res = circuits.get_top_n_largest_sets(3)
    return math.prod(res)


def solve_pt2(data: LoadedDataType) -> int:
    num_connections, junctions = data
    heap = list()
    for l, r in itertools.combinations(junctions, 2):
        item = _compute_distance(l, r), l, r
        heapq.heappush(heap, item)

    circuits = Circuits(junctions)
    num_connections = 0
    while True:
        _, l, r = heapq.heappop(heap)
        num_connections += 1
        if len(junctions) == circuits.merge(l, r):
            return l[0] * r[0]

if __name__ == "__main__":
    FileSolver[LoadedDataType].construct_for_day(
        day_number=8,
        loader=load,
        solutions=[solve_pt1, solve_pt2]
    ).solve_all()
