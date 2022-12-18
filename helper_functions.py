from enum import Enum
from typing import Union, Sequence, Callable, Self, Any, Iterator
import math
import time
from functools import wraps

import numpy as np


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Record the start time
        start_time = time.time()

        # Call the function being decorated
        result = func(*args, **kwargs)

        # Record the end time
        end_time = time.time()

        # Print the elapsed time
        print(f"Elapsed time for {func.__name__}: {end_time - start_time} seconds")

        # Return the result of the decorated function
        return result

    # Return the wrapper function
    return wrapper


class Characters(Enum):
    WHITE_BLOCK = "\u2588"
    BLACK_BLOCK = "\u2591"


def digits_to_int(
    data: Union[Sequence[str], str],
    individual_character: bool = True,
    return_type: Callable = list,
) -> Union[Sequence[Sequence[int]], Sequence[int]]:
    """Converts character digits to ints. Can take both a Sequence of strings
    and a single string as input. It is possible to specify if string should be
    converted as a whole, or if digits should be treated individually.
    For example,
        1. the string "123" is converted to [1, 2, 3] or 123 (individual_character is True or False respectively)
        2. ["123", "456"] is converted to [[1, 2, 3], [4, 5, 6]] or [123, 456]

    Args:
        data:                   The string data to be converted
        individual_character:   If True, each digit in the string is converted
                                as a separate int. Otherwise, the string is
                                taken as a whole.
        return_type:            Specifies what data type the output should be.
                                By default, the function will return lists.
                                This should be a value Sequence type.

    Returns:
        The output will be the same level of nesting as the input, unless
        the digits should be treated individually. In that case, the output is
        nested 1 level more. The data type of the sequence can is user-defined.
    """

    def convert_line(line):
        return return_type(map(int, line)) if individual_character else int(line)

    if isinstance(data, str):
        return convert_line(data)

    return return_type(convert_line(line) for line in data)


def pad_numpy_array(
    np_array: np.ndarray,
    padding_symbol: int,
    pad_width: Union[int, tuple[int, ...], tuple[tuple[int, ...], ...]] = (1,),
) -> np.ndarray:
    """Pad a numpy array with a constant value

    Args:
        np_array:           Array to pad
        padding_symbol:     Value to set the padded values
        pad_width:          Number of values padded to the edges of each axis.
                            ((before_1, after_1), … (before_N, after_N)) unique
                            pad widths for each axis. ((before, after),) yields
                            same before and after pad for each axis. (pad,) or
                            int is a shortcut for before = after = pad width for
                            all axes.
    """
    return np.pad(np_array, pad_width, mode="constant", constant_values=padding_symbol)


def get_sign(number: Union[int, float], sign_zero: int = 0) -> int:
    """Return sign of a number. sign_zero defines what is returned when
    number = 0:
     5 ->  1
    -2 -> -1,
     0 ->  sign_zero
    """
    if number > 0:
        return 1
    elif number < 0:
        return -1
    else:
        return sign_zero


class Coordinate(tuple):
    def __new__(cls, *data) -> Self:
        """Be adding this call we allow coordinate creation via Coordinate(x, y)
        instead of Coordinate((x, y))"""
        assert isinstance(data, tuple), (
            f"Incoming data should have been "
            f"formatted as tuple, actual "
            f"data: {data}"
        )
        if len(data) == 1 and isinstance(data[0], (tuple, list)):
            # If coordinate was instantiated by Coordinate((x, y)) or
            # Coordinate([x, y]), we need to unpack the data. Otherwise, a
            # coordinate is created as ((x, y),).
            # However, we should not catch the case where Coordinate was called
            # as: Coordinate(1)
            data = data[0]
        return super().__new__(cls, data)

    def __add__(self, other: Self) -> Self:
        """Redefine how Coordinates add together"""
        assert len(self) == len(other)
        return Coordinate(*[x + y for x, y in zip(self, other)])

    def __sub__(self, other: Self) -> Self:
        assert len(self) == len(other)
        return Coordinate(*[x - y for x, y in zip(self, other)])

    def __gt__(self, other: Self) -> bool:
        assert len(self) == len(other)
        return all([x > y for x, y in zip(self, other)])

    def __lt__(self, other: Self) -> bool:
        assert len(self) == len(other)
        return all([x < y for x, y in zip(self, other)])

    def __ge__(self, other: Self) -> bool:
        assert len(self) == len(other)
        return all([x >= y for x, y in zip(self, other)])

    def __le__(self, other: Self) -> bool:
        assert len(self) == len(other)
        return all([x <= y for x, y in zip(self, other)])

    def distance(self, other: Self) -> float:
        """Calculate the euclidian distance between two coordinates"""
        return math.sqrt(sum([(x - y) ** 2 for x, y in zip(self, other)]))

    def is_touching(self, other: Self, overlap: bool = True) -> bool:
        """True is self and other are located at most 1 step away for each axis.
        overlap indicates if coordinates are touching when on the same
        coordinate."""
        if not overlap and self == other:
            return False
        return all([abs(x - y) <= 1 for x, y in zip(self, other)])


class Direction(Enum):
    LEFT = Coordinate(0, -1)
    UP = Coordinate(-1, 0)
    RIGHT = Coordinate(0, 1)
    DOWN = Coordinate(1, 0)


class Processor:
    def __init__(self, memory: dict[str, int]) -> None:
        self.memory = memory


class LineSegment:
    def __init__(self, start: Coordinate, end: Coordinate) -> None:
        """Create line segment"""
        if not any([x == y for x, y in zip(start, end)]):
            raise NotImplementedError(
                f"Attempted to create a diagonal line segment with "
                f"{start = } and {end =}. However, this class currently only "
                f"supports horizontal or vertical lines."
            )
        if start >= end:
            # We enforce that the start of a line segment is always smaller
            # than the end
            start, end = end, start
        self.start = start
        self.end = end

    def intersect(self, point: Coordinate) -> bool:
        """Check if point lies on the line segment."""
        # print(f"Intersection? {self.start = }, {point = }, {self.end = }")
        return self.start <= point <= self.end

    def __iter__(self):
        """Return all points in the line segment"""
        direction = tuple(
            get_sign(coordinate, sign_zero=0) for coordinate in self.end - self.start
        )
        point = self.start
        while point <= self.end:
            yield point
            point += direction

    def __repr__(self) -> str:
        return f"{self.start} -> {self.end}"


def yield_next_from_iterator(iterable: Sequence) -> Iterator[Any]:
    """Gets an iterable and perpetually yields from that iterable"""
    idx = 0
    while True:
        yield iterable[idx]
        idx += 1
        if idx >= len(iterable):
            # When we reach the end, reset the index
            idx = 0


def print_grid(grid: np.ndarray, symbols: dict = None) -> None:
    """Prints the grid with the given symbols"""
    default_symbols = {0: Characters.BLACK_BLOCK.value, 1: Characters.WHITE_BLOCK.value,
                       2: "o", 3: "+"}
    if not symbols:
        symbols = default_symbols
    else:
        symbols = default_symbols.update(symbols)

    print()
    for row in grid:
        grid_str = "".join([default_symbols[value] for value in row])
        print(grid_str)