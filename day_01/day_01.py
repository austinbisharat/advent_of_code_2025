from types import NoneType
from typing import Generic

from common.streaming_solver import StreamingSolver, AbstractItemStreamingSolution


FileConfigType = None
ItemDataType = int


def parse_item(line: str) -> ItemDataType:
    prefix, remaining = line[0], int(line[1:])
    return (int(prefix.lower() == "r") * 2 - 1) * remaining


class Part1Solution(AbstractItemStreamingSolution[ItemDataType, FileConfigType]):
    def __init__(self) -> None:
        self._dial_loc = 50
        self._result = 0

    def process_item(self, item: ItemDataType) -> None:
        self._dial_loc = (self._dial_loc + item) % 100
        self._result += int(self._dial_loc == 0)

    def result(self) -> int:
        return self._result


class Part2Solution(AbstractItemStreamingSolution[ItemDataType, FileConfigType]):
    def __init__(self) -> None:
        self._dial_loc = 50
        self._result = 0

    def process_item(self, item: ItemDataType) -> None:
        started_at_zero = self._dial_loc == 0
        self._dial_loc += item
        count_clicks = sum((
            abs(self._dial_loc) // 100,
            int(self._dial_loc < 0 and not started_at_zero),
            int(self._dial_loc == 0),
        ))
        self._result += count_clicks
        self._dial_loc = self._dial_loc % 100

    def result(self) -> int:
        return self._result



if __name__ == "__main__":
    StreamingSolver[ItemDataType, FileConfigType].construct_for_day(
        day_number=1,
        item_parser=parse_item,
        solutions=[Part1Solution, Part2Solution],
    ).solve_all()
