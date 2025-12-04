from typing import TextIO
from common.file_solver import FileSolver
from common.grid import Grid, load_char_grid, ALL_DIRECTIONS

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

    can_remove_more = True
    num_removed = 0
    while can_remove_more:
        can_remove_more = False

        new_grid = grid.copy()
        for grid_point, grid_value in grid.iter_points_and_values():
            if grid_value == PAPER_ROLL_CELL and sum(
                1
                for _, neighbor_value in grid.iter_neighboring_points_and_values(
                    grid_point,
                    directions=ALL_DIRECTIONS,
                )
                if neighbor_value == PAPER_ROLL_CELL
            ) < 4:
                can_remove_more = True
                new_grid[grid_point] = REMOVED_CELL
                num_removed += 1

        grid = new_grid

    return num_removed


if __name__ == "__main__":
    FileSolver[LoadedDataType].construct_for_day(
        day_number=4,
        loader=load_char_grid,
        solutions=[solve_pt1, solve_pt2]
    ).solve_all()
