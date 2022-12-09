from collections import defaultdict
from typing import Optional, Union

from aocd import get_data, submit

import helper_functions
from helper_functions import Coordinate, Direction


DIRECTION_MAP = {
    "L": Direction.LEFT.value,
    "U": Direction.UP.value,
    "R": Direction.RIGHT.value,
    "D": Direction.DOWN.value,
}


def parse_data(load_test_data: bool = False) -> list[str]:
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local
                            directory
    """
    if load_test_data:
        with open("input9.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=9, year=2022)
    lines = data.splitlines()
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return lines


def move_towards(self: Coordinate, other: Coordinate) -> Coordinate:
    """Step self towards other"""
    difference = other - self
    direction = [
        helper_functions.get_sign(coordinate, sign_zero=0) for coordinate in difference
    ]
    return Coordinate(*[coordinate + step for coordinate, step in zip(self, direction)])


def move_tail(location_tail: Coordinate, location_head: Coordinate) -> Coordinate:
    """Move tail towards head. Tail should always be touching the head.
    Diagonally touching or overlapping also count as touching. If not, then the
    tail needs to move towards the head."""
    if location_tail.is_touching(location_head):
        # Don't move the tail
        return location_tail
    return move_towards(location_tail, location_head)


def move(
    command: str,
    locations: list[Coordinate, ...],
    tail_locations: dict[Coordinate, int] = None,
) -> Union[tuple[list[Coordinate, ...], dict[Coordinate, int]], list[Coordinate, ...]]:
    """Move the head. Expected format of command: [direction] [steps]
    direction can be any of [L, U, R, D]"""
    direction, steps = command.split()
    steps = int(steps)
    while steps > 0:
        # Move head
        locations[0] += DIRECTION_MAP[direction]
        # Move tailpieces
        for tail_idx in range(1, len(locations)):
            new_tail_location = move_tail(locations[tail_idx], locations[tail_idx - 1])
            if locations[tail_idx] == new_tail_location:
                # If a tailpiece doesn't move, all tailpieces after that won't
                # move either.
                break
            # Otherwise, store the new location for this tailpiece
            locations[tail_idx] = new_tail_location

        if tail_locations is not None:
            tail_locations[locations[-1]] += 1
        steps -= 1
    if tail_locations is not None:
        return locations, tail_locations
    return locations


def process_commands(
    commands: list[str], length_rope: int = 2, register_tail_locations: bool = False
) -> tuple[dict[str, Coordinate], Optional[dict[Coordinate, int]]]:
    """Process all move commands"""
    if register_tail_locations:
        tail_locations = defaultdict(int)
    else:
        tail_locations = None
    locations = [Coordinate(0, 0)] * length_rope
    for command in commands:
        locations = move(command, locations, tail_locations)
        if register_tail_locations:
            # If we passed tail locations, then we need to unpack the function
            # response
            locations, tail_locations = locations

    return locations, tail_locations


def part1(data: list[str]) -> int:
    """Advent of code 2022 day 9 - Part 1"""
    _, tail_locations = process_commands(data, register_tail_locations=True)
    answer = len(tail_locations)

    print(f"Solution day 9, part 1: {answer}")
    return answer


def part2(data: list[str]) -> int:
    """Advent of code 2022 day 9 - Part 2"""
    _, tail_locations = process_commands(
        data, length_rope=10, register_tail_locations=True
    )
    answer = len(tail_locations)

    print(f"Solution day 9, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input9.1'
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
            submit(aocd_result, part=part, day=9, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    submit_answer = False
    # submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    main("ab", should_submit=submit_answer, load_test_data=test_data)
