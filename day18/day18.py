import re
from typing import Self, Optional

from aocd import get_data, submit
import numpy as np

import helper_functions
from helper_functions import Coordinate


def parse_data(load_test_data: bool = False) -> tuple[tuple[int]]:
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
    return blocks


def get_grid_boundaries(blocks: tuple[tuple[int]]) -> (Coordinate, Coordinate):
    """Get the minimum and maximum coordinate of the 3D space the blocks are
    covering"""
    coordinates_per_axis = list(zip(*blocks))
    space_minimum = Coordinate(*[min(axis) for axis in coordinates_per_axis])
    space_maximum = Coordinate(*[max(axis) for axis in coordinates_per_axis])
    return space_minimum, space_maximum


class Block:
    """Class for blocks in 3 dimensions"""

    # Mapping for other.coordinate - self.coordinate, e.g.
    #   self.coordinate = (0, 0, 0)
    #   other.coordinate = (1, 0, 0)
    # Then other is a bottom neighbour of self
    map_distance_neighbour = {
        Coordinate(1, 0, 0): "bottom",
        Coordinate(-1, 0, 0): "top",
        Coordinate(0, 1, 0): "right",
        Coordinate(0, -1, 0): "left",
        Coordinate(0, 0, 1): "back",
        Coordinate(0, 0, -1): "front",
    }
    neighbour_pairs = {
        "top": "bottom",
        "bottom": "top",
        "left": "right",
        "right": "left",
        "front": "back",
        "back": "front",
    }

    AIR_NEIGHBOUR = 'air'

    def __init__(self, coordinate: Coordinate) -> None:
        if len(coordinate) != 3:
            raise ValueError(
                f"Block is expecting a 3 dimensional coordinate, "
                f"but got {coordinate} instead"
            )
        self.coordinate = coordinate
        self.neighbours = {
            "top": None,
            "bottom": None,
            "left": None,
            "right": None,
            "front": None,
            "back": None,
        }

    def is_neighbour(self, other: Self) -> bool:
        """Check if the other block is a neighbour in cardinal directions only"""
        return self.coordinate.is_touching(other.coordinate, diagonal=False)

    def neighbour_side(self, other: Self) -> Optional[str]:
        """If self and other are neighbours, check on which side they are
        neighbours"""
        if self.is_neighbour(other):
            distance = other.coordinate - self.coordinate
            # Get the side at which the two block are neighbours
            return self.map_distance_neighbour[distance]

        # Other and self are not neighbours
        return None

    def set_neighbour(self, other, neighbour_side) -> None:
        """Link other to self via the given neighbour side"""
        if neighbour_side not in neighbour_side:
            raise KeyError(
                f"Unexpected neighbour_side, got {neighbour_side}, expected one"
                f" of {list(self.neighbours.keys())}."
            )
        if self.neighbours[neighbour_side] is None:
            self.neighbours[neighbour_side] = other
        else:
            raise ValueError(
                f"Trying to set {other.coordinate} as a {neighbour_side} neighbour "
                f"for block {self.coordinate}. But the current block already has a "
                f"{neighbour_side} neighbour: "
                f"{self.neighbours[neighbour_side].coordinate}"
            )

    def set_if_neighbour(self, other: Self) -> None:
        """If two blocks are neighbours, then link the two block instances
        together via the neighbours property"""
        neighbour_side = self.neighbour_side(other)
        if neighbour_side:
            # link other to self at the given neighbour side
            self.set_neighbour(other, neighbour_side)
            # link self to other at the given neighbour sides counterpart
            other.set_neighbour(self, self.neighbour_pairs[neighbour_side])

    def set_air_as_neighbour(self, air_coordinate: set[Coordinate]) -> None:
        """Set air as neighbour"""
        for step_to_neighbour, face in self.map_distance_neighbour.items():
            neighbour_coordinate = step_to_neighbour + self.coordinate
            if neighbour_coordinate in air_coordinate:
                self.neighbours[face] = self.AIR_NEIGHBOUR

    @property
    def open_faces(self) -> int:
        """Count the number of faces that do not have a neighbour"""
        return sum([1 for neighbour in self.neighbours.values() if not neighbour])

    @property
    def faces_exposed_to_air(self) -> int:
        """Count the number of faces that do not have a neighbour"""
        return sum([1 for neighbour in self.neighbours.values() if neighbour == self.AIR_NEIGHBOUR])

    def print_neighbours(self):
        """Print the neighbours"""
        print(f"\nNeighbours for {self.coordinate}:")
        for key, value in self.neighbours.items():
            print(
                f"{key.capitalize()} neighbour: {value.coordinate if value else None}"
            )


def set_all_neighbours(blocks: list[Block]) -> None:
    """Go through all blocks in the list and link neighbouring blocks"""
    for idx in range(len(blocks) - 1):
        block = blocks[idx]
        for other_block in blocks[idx + 1 :]:
            block.set_if_neighbour(other_block)


def count_open_faces(blocks: list[Block]) -> int:
    """Go through all blocks and count how many sides do not have neighbours"""
    return sum([block.open_faces for block in blocks])


def part1(blocks: list[Block]) -> int:
    """Advent of code 2022 day 18 - Part 1"""
    set_all_neighbours(blocks)
    answer = count_open_faces(blocks)
    # for block in blocks:
    #     block.print_neighbours()

    print(f"Solution day 18, part 1: {answer}")
    return answer


def fill_space_with_air(
    starting_location: Coordinate,
    blocks: list[Coordinate],
    space_limits: tuple[Coordinate, Coordinate],
) -> set[Coordinate]:
    """Fill the space around the blocks with air"""
    current_frontier = [starting_location]
    air_coordinates = set(current_frontier)
    while True:
        next_frontier = []
        for frontier_block in current_frontier:
            # The next frontier is all the coordinates that border the current
            # frontier, and that are still open space (i.e. not a block)
            valid_neighbours = [
                block
                for block in helper_functions.get_unvisited_neighbouring_coordinates(
                    frontier_block, space_limits, air_coordinates
                )
                if block not in blocks
            ]
            air_coordinates.update(valid_neighbours)
            next_frontier += valid_neighbours
        if not next_frontier:
            # if the next frontier is empty, then we have filled all the space
            # that we could.
            break
        current_frontier = next_frontier

    return air_coordinates


def set_air_as_neighbours(blocks: list[Block], air_coordinates: set[Coordinate]) -> None:
    """Set air as neighbour for all open faces facing air"""
    for block in blocks:
        block.set_air_as_neighbour(air_coordinates)


def count_faces_exposed_to_air(blocks: list[Block]) -> int:
    """Go through all blocks and count how many sides do not have neighbours"""
    return sum([block.faces_exposed_to_air for block in blocks])


def part2(data: tuple[tuple[int]], blocks: list[Block]):
    """Advent of code 2022 day 18 - Part 2"""
    space_minimum, space_maximum = get_grid_boundaries(data)
    # Pad the grid with extra space so air can surround all the blocks.
    air_padding = (1, 1, 1)
    space_minimum -= air_padding
    space_maximum += air_padding
    block_coordinates = [Coordinate(location) for location in data]
    air_coordinates = fill_space_with_air(
        starting_location=space_minimum,
        blocks=block_coordinates,
        space_limits=(space_minimum, space_maximum),
    )
    # total_number_of_coordinates = 1
    # for axis_length in space_maximum - space_minimum + (1, 1, 1):
    #     total_number_of_coordinates *= axis_length
    # number_of_enclosed_air_particles = (
    #     total_number_of_coordinates - len(air_coordinates) - len(blocks)
    # )

    # Set neighbours of all blocks
    set_all_neighbours(blocks)
    set_air_as_neighbours(blocks, air_coordinates)

    # Get the number of faces without any neighbours, then deduce 6 from that
    # for every air particle enclosed by the blocks
    # total_number_of_exposed_faces = part1(blocks) - 6 * number_of_enclosed_air_particles
    # Calling the part 1 function on blocks will set each blocks neighbour
    # in-place

    answer = count_faces_exposed_to_air(blocks)

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
    blocks = [Block(Coordinate(location)) for location in data]

    for part in parts:
        if part == "a":
            aocd_result = part1(blocks)
        elif part == "b":
            aocd_result = part2(data, blocks)
        else:
            raise ValueError(f"Wrong part chosen, expecting 'a' or 'b': got {part}")

        if should_submit:
            submit(aocd_result, part=part, day=18, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    # submit_answer = False
    submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    main("b", should_submit=submit_answer, load_test_data=test_data)
    # main("ab", should_submit=submit_answer, load_test_data=test_data)
