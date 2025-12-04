from collections import deque
from typing import TextIO
from common.file_solver import FileSolver
from common.grid import Grid, load_char_grid, ALL_DIRECTIONS, PositionType

LoadedDataType = Grid[str]

PAPER_ROLL_CELL = '@'
EMPTY_CELL = '.'
REMOVED_CELL = 'X'


def solve_pt1(grid: LoadedDataType) -> int:
    result = 0
    for grid_point, grid_value in grid.iter_points_and_values():
        if grid_value == PAPER_ROLL_CELL and sum(
            1
            for _, neighbor_value in grid.iter_neighboring_points_and_values(
                grid_point,
                directions=ALL_DIRECTIONS,
            )
            if neighbor_value == PAPER_ROLL_CELL
        ) < 4:
            result += 1
    return result

def solve_pt2(grid: LoadedDataType) -> int:
    counter_grid = Grid[int].create_empty_grid(grid.width, grid.height, default_cell_value=0)
    for grid_point, grid_value in grid.iter_points_and_values():
        if grid_value != PAPER_ROLL_CELL:
            continue
        for neighbor_point in grid.iter_neighboring_points(grid_point, directions=ALL_DIRECTIONS):
            counter_grid[neighbor_point] = counter_grid[neighbor_point] + 1

    rolls_removed: set[PositionType] = set()
    q: deque[PositionType] = deque()

    for grid_point, grid_value in grid.iter_points_and_values():
        if grid_value == PAPER_ROLL_CELL and counter_grid[grid_point] < 4:
            q.append(grid_point)
            rolls_removed.add(grid_point)

    while q:
        cur_point = q.popleft()
        grid[cur_point] = REMOVED_CELL

        for neighbor_point in grid.iter_neighboring_points(cur_point, directions=ALL_DIRECTIONS):
            counter_grid[neighbor_point] = counter_grid[neighbor_point] - 1
            if (
                grid[neighbor_point] == PAPER_ROLL_CELL
                and counter_grid[neighbor_point] < 4
                and neighbor_point not in rolls_removed
            ):
                q.append(neighbor_point)
                rolls_removed.add(neighbor_point)

    return len(rolls_removed)


if __name__ == "__main__":
    FileSolver[LoadedDataType].construct_for_day(
        day_number=4,
        loader=load_char_grid,
        solutions=[solve_pt1, solve_pt2],
    ).solve_all()
