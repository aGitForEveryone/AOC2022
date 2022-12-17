import re
from typing import Iterator

from aocd import get_data, submit
import numpy as np

import helper_functions
from helper_functions import Coordinate


SYMBOL_ROCK = "#"
SYMBOL_AIR = "."


def parse_data(load_test_data: bool = False):
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


def next_rock() -> Iterator[list[str]]:
    """Returns the next rock that will fall down. For part1, loops through a
    list of 5 shapes"""
    rocks = [
        [SYMBOL_ROCK * 4],
        [
            SYMBOL_AIR + SYMBOL_ROCK + SYMBOL_AIR,
            SYMBOL_ROCK * 3,
            SYMBOL_AIR + SYMBOL_ROCK + SYMBOL_AIR,
        ],
        [
            SYMBOL_AIR + SYMBOL_AIR + SYMBOL_ROCK,
            SYMBOL_AIR + SYMBOL_AIR + SYMBOL_ROCK,
            SYMBOL_ROCK * 3,
        ],
        [SYMBOL_ROCK, SYMBOL_ROCK, SYMBOL_ROCK, SYMBOL_ROCK],
        [SYMBOL_ROCK * 2, SYMBOL_ROCK * 2],
    ]
    rock_iterator = helper_functions.yield_next_from_iterator(rocks)
    while True:
        yield next(rock_iterator)


def move_rock_horizontally(
    cur_position: list[Coordinate], jet_direction: str, grid: np.ndarray
) -> Coordinate:
    """Move rock horizontally. If the rock hits the wall or another rock,
    movement is blocked. Rock coordinate is assumed to be
    (left, right, bottom, top)"""
    match jet_direction:
        case "<":
            move = (-1, -1, 0, 0)
        case ">":
            move = (1, 1, 0, 0)
        case _:
            raise ValueError(f"Invalid jet direction, got {jet_direction}")
    next_position = [part_location + move for part_location in cur_position]

    if next_position[0] < 0 or next_position[1] >= grid.shape[1]:
        return cur_position
    # if grid[]


def part1(data: str) -> int:
    """Advent of code 2022 day 17 - Part 1"""
    grid = np.zeros(10000, 7)
    number_of_rocks = 0
    # Grid dimensions work in reverse. The bottom is the end of the array.
    top_rock_position = grid.shape[0] - 1
    jet_directions = jet_direction_data(data)
    for rock in next_rock():
        left_anchor = 2
        _anchor = top_rock_position - 3 - len(rock) + 1
        rock_coordinates = []
        for line_idx, line in enumerate(rock):
            for char_idx, char in line:
                if char == SYMBOL_ROCK:
                    # left, right, bottom, top
                    rock_coordinates += [
                        Coordinate(
                            left_anchor + char_idx,
                            left_anchor + char_idx + len(rock[0]) - 1,
                            top_anchor - line_idx + len(rock) - 1,
                            top_anchor - line_idx,
                        )
                    ]
        while True:
            jet = next(jet_directions)

        number_of_rocks += 1
        if number_of_rocks == 2022:
            # stop when 2022 rocks have fallen
            break
    answer = 0
    print(data)

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
