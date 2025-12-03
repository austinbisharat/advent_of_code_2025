import abc
from numbers import Number
from typing import Generic, TypeVar, Callable, Type, Any, TextIO, Optional, Iterable

FileConfigType = TypeVar("FileConfigType")
ItemDataType = TypeVar('ItemDataType')
ItemOutputType = TypeVar('ItemOutputType')
ResultType = TypeVar('ResultType')


class AbstractItemStreamingSolution(abc.ABC, Generic[ItemDataType, FileConfigType]):
    @abc.abstractmethod
    def __init__(self) -> None:
        ...

    def load_config(self, config: FileConfigType) -> None:
        pass

    @abc.abstractmethod
    def process_item(self, item: ItemDataType) -> None:
        ...

    @abc.abstractmethod
    def result(self) -> str | int:
        ...


def create_summing_solution(
    item_processor: Callable[[ItemDataType], Number]
) -> Type[AbstractItemStreamingSolution[ItemDataType, None]]:
    return create_streaming_aggregating_solution(
        item_processor=item_processor,
        reducer_func=lambda result, item_result: result + item_result,
        initial_result=0,
    )


def create_product_solution(
    item_processor: Callable[[ItemDataType], Number]
) -> Type[AbstractItemStreamingSolution[ItemDataType, None]]:
    return create_streaming_aggregating_solution(
        item_processor=item_processor,
        reducer_func=lambda result, item_result: result * item_result,
        initial_result=1,
    )


def create_streaming_aggregating_solution(
    item_processor: Callable[[ItemDataType], ItemOutputType],
    reducer_func: Callable[[ResultType, ItemOutputType], ResultType],
    initial_result: ResultType,
) -> Type[AbstractItemStreamingSolution[ItemDataType, None]]:
    class ItemStreamingSolution(AbstractItemStreamingSolution[ItemDataType, None]):
        def __init__(self) -> None:
            self._result = initial_result

        def process_item(self, item: ItemDataType) -> None:
            self._result = reducer_func(self._result, item_processor(item))

        def result(self) -> int:
            return self._result

    return ItemStreamingSolution


class StreamingSolver(Generic[ItemDataType, FileConfigType]):
    def __init__(
        self,
        file_names: list[str],
        item_parser: Callable[[str], ItemDataType],
        solutions: list[Type[AbstractItemStreamingSolution[ItemDataType, FileConfigType]]],
        file_config_parser: Optional[Callable[[TextIO], FileConfigType]] = None,
        log_func: Callable[[Any], None] = print,
        item_delimiter: str | None = None,
    ) -> None:
        self._file_names = file_names
        self._item_parser = item_parser
        self._solution_classes = solutions
        self._file_config_parser = file_config_parser
        self._log_func = log_func
        self._item_delimiter = item_delimiter

    @classmethod
    def construct_for_day(
        cls,
        day_number: int,
        item_parser: Callable[[str], ItemDataType],
        solutions: list[Type[AbstractItemStreamingSolution[ItemDataType, FileConfigType]]],
        file_config_parser: Optional[Callable[[TextIO], FileConfigType]] = None,
        log_func: Callable[[Any], None] = print,
        item_delimiter: str | None = None,
    ) -> 'StreamingSolver[ItemDataType, FileConfigType]':
        return cls(
            file_names=[f'sample_{day_number:02d}.txt', f'input_{day_number:02d}.txt'],
            item_parser=item_parser,
            solutions=solutions,
            file_config_parser=file_config_parser,
            log_func=log_func,
            item_delimiter=item_delimiter,
        )

    def solve_all(self) -> None:
        for file_name in self._file_names:
            self.solve_file(file_name)

    def solve_file(self, file_name: str) -> None:
        self._log_func(f'Solving {file_name}:')
        solutions = [s() for s in self._solution_classes]

        with open(file_name, 'r') as f:
            if self._file_config_parser:
                file_config = self._file_config_parser(f)
                for solution in solutions:
                    solution.load_config(file_config)

            for item in self._stream_items_from_file(f):
                self._process_item(item, solutions)

        for i, solution in enumerate(solutions):
            result = solution.result()
            self._log_func(f'\tSolution for part {i + 1}: {result}')
        self._log_func(f'Done.\n')

    def _stream_items_from_file(self, file: TextIO, chunk_size=256) -> Iterable[str]:
        if self._item_delimiter is None:
            yield from file
            return

        buffer = ""
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break

            buffer += chunk
            while (pos := buffer.find(self._item_delimiter)) != -1:
                yield buffer[:pos]
                buffer = buffer[pos + len(self._item_delimiter):]

        if buffer:
            yield buffer

    def _process_item(
        self,
        item_str: str,
        solutions: list[AbstractItemStreamingSolution[ItemDataType, FileConfigType]],
    ) -> None:
        parsed_item = self._item_parser(item_str)

        for i, solution in enumerate(solutions):
            solution.process_item(parsed_item)
