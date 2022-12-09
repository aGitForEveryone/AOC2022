import re

from aocd import get_data, submit
import numpy as np


COORDINATE = tuple[int, int]


def parse_data(load_test_data: bool = False):
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
    return data


def move_tail(location_tail: COORDINATE, location_head: COORDINATE) -> COORDINATE:
    """Move tail towards head. Tail should always be touching the head.
    Diagonally touching or overlapping also count as touching. If not, then the
    tail needs to move towards the head."""



def move(command: str, locations: dict[str, tuple[int]]):
    """Move the head. Expected format of command: [direction] [steps]
    direction can be any of [L, U, R, D]"""
    direction, steps = command.split()
    steps = int(steps)


def part1(data):
    """Advent of code 2022 day 9 - Part 1"""
    answer = 0
    print(data)

    print(f"Solution day 9, part 1: {answer}")
    return answer


def part2(data):
    """Advent of code 2022 day 9 - Part 2"""
    answer = 0

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
    main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    # main("ab", should_submit=submit_answer, load_test_data=test_data)
