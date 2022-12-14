import re

from aocd import get_data, submit
import numpy as np

import helper_functions
from helper_functions import LineSegment, Coordinate


VOID = Coordinate(-100, -100)
SAND_ENTRY = Coordinate(500, 0)


def parse_data(load_test_data: bool = False) -> list[str]:
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local
                            directory
    """
    if load_test_data:
        with open("input14.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=14, year=2022)
    lines = data.splitlines()
    # grid = np.array(helper_functions.digits_to_int(data.splitlines()))
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return lines


def build_line_segments(data: list[str]) -> (list[LineSegment], int):
    """From the input collect all rock line segments in the cavern"""
    line_segments = []
    start_of_void = 0
    for line in data:
        coordinates = []
        for coordinate in line.split(" -> "):
            new_coordinate = Coordinate(
                [int(number) for number in coordinate.split(",")]
            )
            # Check if the row number of the new coordinate is further away
            # from the starting point than what is currently known. The furthest
            # point will mark the start of the void.
            start_of_void = max(start_of_void, new_coordinate[1] + 1)
            coordinates += [new_coordinate]

        for start, end in zip(coordinates[:-1], coordinates[1:]):
            line_segments += [LineSegment(start, end)]
    return line_segments, start_of_void


def get_grid_dimensions(raw_data: str) -> (int, int, int):
    """Get the height and width of the section containing rocks. Also return the
    left most coordinate, so we can shift all coordinates close to 0"""
    # Coordinates are numbers separated by a comma in the original input
    coordinates = re.findall('(\d+),(\d+)', raw_data)
    col, row = zip(*coordinates)
    col = list(map(int, col))
    row = list(map(int, row))
    left = min(col)
    # We add 2 to the height to take into account that the floor is located two
    # lines under the furthest row
    height = max(row) + 1 + 2
    width = max(col) - min(col) + 1
    return height, width, left


def construct_grid(line_segments: list[LineSegment], height: int) -> np.ndarray:
    """Construct a numpy array representation of the rocky cavern. The size of
    the grid will be height x (2 * (height - 2) + 1). As for part 2 the final
    sand layout is a triangle starting at the SAND_ENTRY and ending at the
    bottom. The width of that triangle at the bottom will be a function of the
    grid height."""
    grid = np.zeros((height, (2 * (height - 2) + 1)))
    # For example, in the puzzle example the grid height (including floor and
    # sand entry row) is 12. The sand entry is located in (500, 0) and the left
    # most sand particle is located at (490, 10). So the column shift should be
    # 500 - (12 - 2) for the left most particle to be in the 0th column
    column_shift = SAND_ENTRY[0] - (height - 2)
    for line in line_segments:
        for col, row in line:
            grid[row][col - column_shift] = 1
    grid[SAND_ENTRY[1]][height - 2] = 3
    return grid


def print_grid(grid: np.ndarray, symbols: dict = None) -> None:
    """Prints the grid with the given symbols"""
    grid_symbols = {
        0: '.',
        1: '#',
        2: 'o',
        3: '+'
    }
    if not symbols:
        symbols = grid_symbols
    else:
        symbols = grid_symbols.update(symbols)

    print()
    for row in grid:
        grid_str = "".join([grid_symbols[value] for value in row])
        print(grid_str)


def is_particle_blocked(
    potential_location: Coordinate,
    line_segments: list[LineSegment],
    sand_particles_in_rest: set[Coordinate],
) -> bool:
    """Check if the potential location is free for the sand particle to move in.
    If it contains rock or sand, then it is not."""
    if potential_location in sand_particles_in_rest:
        # We hit sand!
        return True
    for line_segment in line_segments:
        if line_segment.intersect(potential_location):
            # We hit rock!
            return True

    # Nothing stopping us!
    return False


def drop_sand_particle(
    particle_location: Coordinate,
    start_of_void: int,
    line_segments: list[LineSegment],
    sand_particles_in_rest: set[Coordinate],
) -> Coordinate:
    """Drops a sand particle from the start location and find the resting place.
    If the sand particle cannot find a resting place, i.e. it's row number has
    reached the start of the void, then we exit the function."""
    while particle_location[1] < start_of_void:
        next_location = particle_location + (0, 1)
        # print(f"{next_location = }")
        if is_particle_blocked(next_location, line_segments, sand_particles_in_rest):
            # Straight down didn't work, try diagonal left from current particle
            # location instead
            next_location += (-1, 0)
            if is_particle_blocked(
                next_location, line_segments, sand_particles_in_rest
            ):
                # Diagonal left didn't work, let's try diagonal right instead
                next_location += (2, 0)
                if is_particle_blocked(
                    next_location, line_segments, sand_particles_in_rest
                ):
                    # We are blocked all the way, sand particle has come to rest
                    return particle_location
        particle_location = next_location
    return particle_location


def fill_cavern(
    start_location: Coordinate,
    start_of_void: int,
    line_segments: list[LineSegment],
    stop_condition: Coordinate,
) -> int:
    """Keep flooding the cavern with sand until one particle reaches the stop
    condition.
    Return the number of sand particles that came to rest in the cavern"""
    sand_particles_in_rest = set()
    # Keep dropping sand particles, until one reaches the stop condition
    while (
        (
            final_location := drop_sand_particle(
                start_location, start_of_void, line_segments, sand_particles_in_rest
            )
        )
        != stop_condition
    ) or (stop_condition == VOID and final_location[1] < start_of_void):
        sand_particles_in_rest.add(final_location)

    if stop_condition != VOID:
        # The location of the stop condition was not added to the set of sand
        # particles in rest. When dealing with the void, particles will stream
        # forever, so we should ignore the stop condition. Otherwise, a particle
        # will end up in the location of the stop condition, and we add it here.
        sand_particles_in_rest.add(stop_condition)

    return len(sand_particles_in_rest)


def part1(data: list[str]) -> int:
    """Advent of code 2022 day 14 - Part 1"""
    line_segments, start_of_void = build_line_segments(data)
    stop_condition = VOID
    answer = fill_cavern(SAND_ENTRY, start_of_void, line_segments, stop_condition)

    print(f"Solution day 14, part 1: {answer}")
    return answer


def part2(data):
    """Advent of code 2022 day 14 - Part 2"""
    line_segments, start_of_void = build_line_segments(data)
    stop_condition = SAND_ENTRY
    answer = fill_cavern(SAND_ENTRY, start_of_void, line_segments, stop_condition)

    print(f"Solution day 14, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input14.1'
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
            submit(aocd_result, part=part, day=14, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    # submit_answer = False
    submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    main("b", should_submit=submit_answer, load_test_data=test_data)
    # main("ab", should_submit=submit_answer, load_test_data=test_data)
