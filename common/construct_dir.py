import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()

FULL_FILE_SOLVER_TEMPLATE = """from typing import TextIO
from common.file_solver import FileSolver


LoadedDataType = ...


def load(file: TextIO) -> LoadedDataType:
    ...


def solve_pt1(data: LoadedDataType) -> int:
    ...


def solve_pt2(data: LoadedDataType) -> int:
    return 0


if __name__ == "__main__":
    FileSolver[LoadedDataType].construct_for_day(
        day_number={day_num},
        loader=load,
        solutions=[solve_pt1, solve_pt2]
    ).solve_all()
"""

STREAMING_SOLVER_TEMPLATE = """from common.streaming_solver import StreamingSolver, AbstractItemStreamingSolution

FileConfigType = None
LineDataType = ...


def parse_item(item_str: str) -> LineDataType:
    ...


class Part1Solution(AbstractItemStreamingSolution[LineDataType, FileConfigType]):
    def __init__(self) -> None:
        ...

    def process_item(self, line: LineDataType) -> None:
        ...

    def result(self) -> int:
        ...


class Part2Solution(AbstractItemStreamingSolution[LineDataType, FileConfigType]):
    def __init__(self) -> None:
        ...

    def process_item(self, line: LineDataType) -> None:
        ...

    def result(self) -> int:
        ...


if __name__ == "__main__":
    StreamingSolver[LineDataType, FileConfigType].construct_for_day(
        day_number={day_num},
        item_parser=parse_item,
        solutions=[Part1Solution, Part2Solution]
    ).solve_all()
"""

SUMMING_TEMPLATE = """from common.streaming_solver import StreamingSolver, create_summing_solution


LineDataType = ...


def parse_item(item_str: str) -> LineDataType:
    ...


def part_one(data: LineDataType) -> int:
    ...


def part_two(data: LineDataType) -> int:
    ...


if __name__ == "__main__":
    StreamingSolver[LineDataType, None].construct_for_day(
        day_number={day_num},
        item_parser=parse_item,
        solutions=[
            create_summing_solution(part_one),
            create_summing_solution(part_two)
        ]
    ).solve_all()
"""

TEMPLATES = {
    'FILE': FULL_FILE_SOLVER_TEMPLATE,
    'STREAMING': STREAMING_SOLVER_TEMPLATE,
    'SUMMING': SUMMING_TEMPLATE,
}


def construct_dir(
    day_number: int,
    template: str,
    option: str = 'x'
) -> None:
    directory = BASE_DIR / f"day_{day_number:02d}"
    directory.mkdir(exist_ok=True)
    open(directory / f'input_{day_number:02d}.txt', 'x').close()
    open(directory / f'sample_{day_number:02d}.txt', 'x').close()
    with open(directory / f'day_{day_number:02d}.py', option) as main_file:
        main_file.write(template.format(day_num=day_number))


if __name__ == '__main__':
    day_number = input("Enter day number: ")
    templates = '\n\t'.join(TEMPLATES.keys())
    template_name = input(f"Template Options:\n\t{templates}\nEnter template name: ").strip().upper()

    if not template_name:
        template_name = 'STREAMING'

    flag = input('Enter template flag (w=overwrite, x=create_or_err): ')
    construct_dir(
        day_number=int(day_number),
        template=TEMPLATES[template_name.strip().upper()],
        option=flag or 'x',
    )
