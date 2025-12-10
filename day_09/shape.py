import dataclasses
import itertools
import sys
import bisect
from collections import deque, defaultdict
from typing import Iterable

from common.grid import PositionType, Direction, get_turns_between_directions, get_cardinal_dir_between_points, \
    rotate_90, CARDINAL_DIRS, ALL_DIRECTIONS, add_relative_point

RectType = tuple[PositionType, PositionType]

@dataclasses.dataclass(frozen=True, order=True)
class Line:
    axis_loc: int
    on_axis_start: int
    on_axis_end: int

@dataclasses.dataclass
class RightAnglePolyData:
    vertices: list[PositionType]
    sorted_vertical_lines: list[Line]
    sorted_horizontal_lines: list[Line]
    corner_adj_data: dict[PositionType, list[Direction]]
    sorted_corners_by_row: dict[int, list[PositionType]]
    sorted_corners_by_col: dict[int, list[PositionType]]
    interior_turns: int


def get_areas_for_possible_rects(vertices: list[PositionType]) -> Iterable[int]:
    _validate_no_points_too_close(vertices)

    poly_data = _preprocess_right_angle_poly(vertices)

    vertex_to_max_bounding_rect: dict[PositionType, RectType] = {
        point: _get_max_bounding_rect_for_corner(point, poly_data)
        for point in vertices
    }
    for v1, v2 in itertools.combinations(vertices, 2):
        v1_bounding_rect = vertex_to_max_bounding_rect[v1]
        v2_bounding_rect = vertex_to_max_bounding_rect[v2]
        if _bounding_rect_contains_point(v1, v2_bounding_rect) and _bounding_rect_contains_point(v2, v1_bounding_rect):
            yield _area((v1, v2))


def _validate_no_points_too_close(points: list[PositionType]) -> None:
    # The rest of the solution relies on the potentially unsafe assumption that none of the lines that form
    # the polygon are directly adjacent
    all_points = set(points)
    for p, d in itertools.product(all_points, ALL_DIRECTIONS):
        adj = add_relative_point(p, d.value)
        if adj in all_points:
            raise Exception('overlap')


def _preprocess_right_angle_poly(vertices: list[PositionType]) -> RightAnglePolyData:
    turns = 0
    last_dir: Direction | None = None

    vertical_lines: deque[Line] = deque()
    horizontal_lines: deque[Line] = deque()
    corners_and_turns: deque[tuple[PositionType, Direction, int]] = deque()
    corners_by_row: dict[int, list[PositionType]] = defaultdict(list)
    corners_by_col: dict[int, list[PositionType]] = defaultdict(list)

    for i, (cur_v, next_v) in enumerate(itertools.pairwise(vertices + vertices[:2])):
        if i < len(vertices):
            corners_by_row[cur_v[0]].append(cur_v)
            corners_by_col[cur_v[1]].append(cur_v)

        cur_dir = get_cardinal_dir_between_points(cur_v, next_v)
        if last_dir is not None:
            cur_turn = get_turns_between_directions(last_dir, cur_dir)
            corners_and_turns.append((cur_v, cur_dir, cur_turn))

            if i < len(vertices)+1:
                turns += cur_turn

        last_dir = cur_dir

        if cur_dir in (Direction.NORTH, Direction.SOUTH):
            vertical_lines.append(Line(
                axis_loc=cur_v[1],
                on_axis_start=min(cur_v[0], next_v[0]),
                on_axis_end=max(cur_v[0], next_v[0]),
            ))
        else:
            horizontal_lines.append(Line(
                axis_loc=cur_v[0],
                on_axis_start=min(cur_v[1], next_v[1]),
                on_axis_end=max(cur_v[1], next_v[1]),
            ))


    assert last_dir is not None
    assert abs(turns) == 4
    avg_turn = turns // 4


    # For each corner, store the set of cardinal directions that will
    # be on the interior of the polygon
    corner_adj_data: dict[PositionType, list[Direction]] = {
        cur_v: (
            [cur_dir, rotate_90(cur_dir, t)]
            if t == avg_turn
            else CARDINAL_DIRS
        )
        for cur_v, cur_dir, t in corners_and_turns
    }

    for l in corners_by_row.values():
        l.sort()

    for l in corners_by_col.values():
        l.sort()

    # noinspection PyTypeChecker
    return RightAnglePolyData(
        vertices=sorted(vertices),
        sorted_vertical_lines=sorted(vertical_lines),
        sorted_horizontal_lines=sorted(horizontal_lines),
        interior_turns=avg_turn,
        corner_adj_data=corner_adj_data,
        sorted_corners_by_row=corners_by_row,
        sorted_corners_by_col=corners_by_col,
    )


def _area(rect: RectType):
    (top_row, top_col), (bot_row, bot_col) = rect
    return (abs(top_row - bot_row) + 1) * (abs(top_col - bot_col) + 1)


def _get_furthest_interior_point_along_dir(
    corner: PositionType,
    direction: Direction,
    poly_data: RightAnglePolyData,
) -> PositionType:
    sign = sum(direction.value)
    is_ray_vertical = direction in (Direction.NORTH, Direction.SOUTH)

    potentially_intersecting_lines = poly_data.sorted_horizontal_lines if is_ray_vertical else poly_data.sorted_vertical_lines

    row, col = corner

    ray_start_loc = row if is_ray_vertical else col
    ray_on_axis_loc = col if is_ray_vertical else row

    if sign < 0:
        # noinspection PyTypeChecker
        start_idx = bisect.bisect_right(potentially_intersecting_lines, Line(
            axis_loc=ray_start_loc,
            on_axis_start=-1,
            on_axis_end=-1,
        ))
        end_idx = -1
    else:
        # noinspection PyTypeChecker
        start_idx = bisect.bisect_left(potentially_intersecting_lines, Line(
            axis_loc=ray_start_loc,
            on_axis_start=sys.maxsize,
            on_axis_end=sys.maxsize,
        ))
        end_idx = len(potentially_intersecting_lines)


    def _construct_point_on_ray(potential_ray_end: int) -> tuple[int, int]:
        return (
            (potential_ray_end, ray_on_axis_loc)
            if is_ray_vertical
            else (ray_on_axis_loc, potential_ray_end)
        )

    def _check_if_corner_is_terminal(potential_ray_end: int) -> bool:
        potential_terminal_corner = _construct_point_on_ray(potential_ray_end)
        corner_adj_data = poly_data.corner_adj_data[potential_terminal_corner]
        return direction not in corner_adj_data

    for line_idx in range(start_idx, end_idx, sign):
        line = potentially_intersecting_lines[line_idx]
        if (
            line.on_axis_start < ray_on_axis_loc < line.on_axis_end
            or (
                ray_on_axis_loc in (line.on_axis_start, line.on_axis_end)
                and _check_if_corner_is_terminal(line.axis_loc)
           )
        ):
            return _construct_point_on_ray(line.axis_loc)

    raise ValueError('Should not ever get here')


def _get_candidate_rects_for_corner(corner: PositionType, poly_data: RightAnglePolyData) -> Iterable[RectType]:
    for direction in poly_data.corner_adj_data[corner]:
        pass


def _get_max_bounding_rect_for_corner(corner: PositionType, poly_data: RightAnglePolyData) -> RectType:
    extreme_corners = [corner] + [
        _get_furthest_interior_point_along_dir(corner, direction, poly_data)
        for direction in poly_data.corner_adj_data[corner]
    ]
    row_vals, col_vals = zip(*extreme_corners)


    top_left = min(row_vals), min(col_vals)
    bottom_right = max(row_vals), max(col_vals)
    return top_left, bottom_right


def _bounding_rect_contains_point(vertex: PositionType, rect: RectType) -> bool:
    row, col = vertex
    (min_row, min_col), (max_row, max_col) = rect
    return min_row <= row <= max_row and min_col <= col <= max_col
