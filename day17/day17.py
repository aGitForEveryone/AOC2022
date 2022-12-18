import re
from typing import Iterator, Sequence, Optional

from aocd import get_data, submit
import numpy as np

import helper_functions
from helper_functions import Coordinate


SYMBOL_ROCK = "#"
SYMBOL_AIR = "."

POSSIBLE_ROCKS = [
    tuple((SYMBOL_ROCK * 4,)),
    tuple(
        (
            SYMBOL_AIR + SYMBOL_ROCK + SYMBOL_AIR,
            SYMBOL_ROCK * 3,
            SYMBOL_AIR + SYMBOL_ROCK + SYMBOL_AIR,
        )
    ),
    tuple(
        (
            SYMBOL_AIR + SYMBOL_AIR + SYMBOL_ROCK,
            SYMBOL_AIR + SYMBOL_AIR + SYMBOL_ROCK,
            SYMBOL_ROCK * 3,
        )
    ),
    tuple((SYMBOL_ROCK, SYMBOL_ROCK, SYMBOL_ROCK, SYMBOL_ROCK)),
    tuple((SYMBOL_ROCK * 2, SYMBOL_ROCK * 2)),
]

ROCK = tuple[str]
ROCK_LOCATION = list[Coordinate]


def initial_position_rocks(
    rocks: list[ROCK], bottom_left_anchor: Coordinate
) -> dict[ROCK, ROCK_LOCATION]:
    """Return the position for each rock if it were to spawn on an empty grid"""
    initial_positions = {}
    for rock_shape in rocks:
        rock_parts = []
        # Create the coordinate of each rock part in the rock shape
        # Coordinates work in reverse in grid, moving up is a smaller row
        # coordinate
        for line_idx, line in enumerate(rock_shape):
            for char_idx, char in enumerate(line):
                if char == SYMBOL_ROCK:
                    rock_parts += [
                        bottom_left_anchor + (line_idx - len(rock_shape) + 1, char_idx)
                    ]

        initial_positions[rock_shape] = rock_parts

    return initial_positions


# Every rock spawns in the cavern with its left most position 2 from the edge
# and its bottom most position 3 from the highest rock. The initial height
# for each rock is determined assuming the highest rock is at location 0. During
# the actual rock spawn, the height can be adjusted by shifting the rock up and
# down depending on the current state of the cavern.
INITIAL_POSITIONS_ROCK = initial_position_rocks(POSSIBLE_ROCKS, Coordinate(0, 2))


def parse_data(load_test_data: bool = False) -> str:
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local
                            directory
    """
    if load_test_data:
        with open("input17.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=17, year=2022)
    # lines = data.splitlines()
    # grid = np.array(helper_functions.digits_to_int(data.splitlines()))
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return data


def jet_direction_data(jet_streams: str) -> Iterator[str]:
    """Yields the next direction of the jet stream. Will loop through all
    characters in jet_streams. If the end of the available directions is
    reached, then iteration starts from the beginning again."""

    jet_stream_iterator = helper_functions.yield_next_from_iterator(jet_streams)
    while True:
        yield next(jet_stream_iterator)


def next_rock(rocks: Sequence[ROCK]) -> Iterator[ROCK]:
    """Returns the next rock that will fall down. For part1, loops through a
    list of 5 shapes"""
    rock_iterator = helper_functions.yield_next_from_iterator(rocks)
    while True:
        yield next(rock_iterator)


def is_valid_location(cur_position: ROCK_LOCATION, cavern: np.ndarray) -> bool:
    """Check if the current position is a valid location for the rock"""
    grid_shape = Coordinate(cavern.shape)

    for part_location in cur_position:
        part_in_grid = Coordinate(0, 0) <= part_location < grid_shape
        # in the numpy representation of the cavern, 0 means empty space, and 1
        # means occupied space. The check of the grid status is moved inside the
        # conditional to make sure that is only check when part location is on
        # the grid.
        if not part_in_grid or cavern[part_location]:
            return False

    return True


def move_rock(
    cur_position: ROCK_LOCATION, step: Coordinate, cavern: np.ndarray
) -> ROCK_LOCATION:
    """Move the rock by the given step"""
    next_position = [part_location + step for part_location in cur_position]
    if is_valid_location(next_position, cavern):
        return next_position
    return cur_position


def move_rock_horizontally(
    cur_position: ROCK_LOCATION, jet_direction: str, cavern: np.ndarray
) -> ROCK_LOCATION:
    """Move rock horizontally. If the rock hits the wall or another rock,
    movement is blocked. Rock coordinate is assumed to be
    (left, right, bottom, top)"""
    match jet_direction:
        case "<":
            move = Coordinate(0, -1)
        case ">":
            move = Coordinate(0, 1)
        case _:
            raise ValueError(f"Invalid jet direction, got {jet_direction}")

    # Move all parts of the block
    return move_rock(cur_position, move, cavern)


def move_rock_down(cur_position: ROCK_LOCATION, cavern: np.ndarray) -> ROCK_LOCATION:
    """Move the rock down."""
    return move_rock(cur_position, Coordinate(1, 0), cavern)


def get_highest_rock_point(cur_position: ROCK_LOCATION) -> int:
    """Get the highest point of the rock (which is the lowest row coordinate)"""
    return min([part_location[0] for part_location in cur_position])


def place_rock_in_cavern(rock_position: ROCK_LOCATION, cavern: np.ndarray, value: int = 1) -> None:
    """Places the rock in the cavern. Update is done in-place on the cavern.
    Every location where there is a rock part, the grid value will be a 1"""
    for part_location in rock_position:
        cavern[part_location] = value


def part1(data: str) -> int:
    """Advent of code 2022 day 17 - Part 1"""
    cavern = np.zeros((3200, 7))
    number_of_rocks = 0
    # Grid dimensions work in reverse. The bottom is the end of the array.
    top_rock_position = cavern.shape[0]
    jet_directions = jet_direction_data(data)
    rocks = next_rock(POSSIBLE_ROCKS)

    for rock in rocks:
        cur_position = move_rock(
            INITIAL_POSITIONS_ROCK[rock], Coordinate(top_rock_position - 4, 0), cavern
        )

        while True:
            # Rocks move in two steps: first horizontally due to jet streams,
            # and then it moves down
            jet = next(jet_directions)
            position_after_jet = move_rock_horizontally(cur_position, jet, cavern)
            cur_position = move_rock_down(position_after_jet, cavern)
            # print_cavern = cavern.copy()
            # place_rock_in_cavern(cur_position, print_cavern, 2)
            # helper_functions.print_grid(print_cavern[9985:, :])
            if cur_position[0] == position_after_jet[0]:
                # If the block didn't move during the move down step, the block
                # comes to rest. Perform the exit logic.
                highest_rock_point = get_highest_rock_point(cur_position)
                top_rock_position = min(highest_rock_point, top_rock_position)
                place_rock_in_cavern(cur_position, cavern)
                break

        # helper_functions.print_grid(cavern[9985:, :])
        number_of_rocks += 1
        if number_of_rocks == 2022:
            # stop when 2022 rocks have fallen
            break
    answer = cavern.shape[0] - top_rock_position

    print(f"Solution day 17, part 1: {answer}")
    return answer


def part2(data):
    """Advent of code 2022 day 17 - Part 2"""
    answer = 0

    print(f"Solution day 17, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input17.1'
    """
    data = parse_data(load_test_data=load_test_data)

    for part in parts:
        if part == "a":
            aocd_result = part1(data)
        elif part == "b":
            aocd_result = part2(data)
        else:
            raise ValueError(f"Wrong part chosen, expecting 'a' or 'b': got {part}")

        if should_submit:
            submit(aocd_result, part=part, day=17, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    submit_answer = False
    # submit_answer = True
    main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    # main("ab", should_submit=submit_answer, load_test_data=test_data)
