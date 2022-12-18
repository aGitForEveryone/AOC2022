import re
from typing import Callable

from aocd import get_data, submit

import helper_functions
from helper_functions import Coordinate


def parse_data(load_test_data: bool = False) -> set[Coordinate]:
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local
                            directory
    """
    if load_test_data:
        with open("input18.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=18, year=2022)
    blocks = helper_functions.digits_to_int(
        re.findall("(\d+),(\d+),(\d+)", data),
        individual_character=False,
        return_type=tuple,
    )
    # lines = data.splitlines()
    # grid = np.array(helper_functions.digits_to_int(data.splitlines()))
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return set([Coordinate(block) for block in blocks])


STEP_TO_NEIGHBOURS = {
    Coordinate(1, 0, 0),
    Coordinate(-1, 0, 0),
    Coordinate(0, 1, 0),
    Coordinate(0, -1, 0),
    Coordinate(0, 0, 1),
    Coordinate(0, 0, -1),
}


def get_open_faces(blocks: set[Coordinate]) -> list[Coordinate]:
    """Return the coordinates of all air tiles next to the blocks, i.e. every
    blocks' neighbouring cell that does not contain a block. Coordinates can
    appear multiple times, if a cell is neighbouring multiple blocks."""
    # For each block, collect all neighbouring coordinates and check that that
    # neighbour cell is not a block
    return [
        neighbour_coordinate
        for block in blocks
        for step in STEP_TO_NEIGHBOURS
        if (neighbour_coordinate := block + step) not in blocks
    ]


def part1(blocks: set[Coordinate]) -> int:
    """Advent of code 2022 day 18 - Part 1"""
    answer = len(get_open_faces(blocks))

    print(f"Solution day 18, part 1: {answer}")
    return answer


def get_grid_boundaries(blocks: set[Coordinate]) -> (Coordinate, Coordinate):
    """Get the minimum and maximum coordinate of the 3D space the blocks are
    covering"""
    coordinates_per_axis = list(zip(*blocks))
    space_minimum = Coordinate(*[min(axis) for axis in coordinates_per_axis])
    space_maximum = Coordinate(*[max(axis) for axis in coordinates_per_axis])
    return space_minimum, space_maximum


def valid_air_coordinate(
    blocks: set[Coordinate],
    space_limits: tuple[Coordinate, Coordinate],
) -> Callable:
    """Function to pass to the flood_fill function. Checks whether a coordinate
    is a valid coordinate for air to fill into"""

    def is_valid_air_coordinate(coordinate: Coordinate) -> bool:
        """Returns True if air can fill in this coordinate"""
        return (
            space_limits[0] <= coordinate <= space_limits[1]
            and coordinate not in blocks
        )

    return is_valid_air_coordinate


def part2(blocks: set[Coordinate]) -> int:
    """Advent of code 2022 day 18 - Part 2"""
    space_minimum, space_maximum = get_grid_boundaries(blocks)
    # Pad the grid with extra space so air can surround all the blocks.
    air_padding = (1, 1, 1)
    space_minimum -= air_padding
    space_maximum += air_padding
    air_coordinates = helper_functions.flood_fill(
        starting_location=space_minimum,
        is_valid_coordinate=valid_air_coordinate(
            blocks, (space_minimum, space_maximum)
        ),
    )
    open_faces = get_open_faces(blocks)

    answer = len(
        [coordinate for coordinate in open_faces if coordinate in air_coordinates]
    )

    print(f"Solution day 18, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input18.1'
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
            submit(aocd_result, part=part, day=18, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    submit_answer = False
    # submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    main("ab", should_submit=submit_answer, load_test_data=test_data)
