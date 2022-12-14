import re

from aocd import get_data, submit
import numpy as np

import helper_functions
from helper_functions import LineSegment, Coordinate


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


def build_line_segments(data: list[str]) -> list[LineSegment]:
    """From the input collect all rock line segments in the cavern"""
    line_segments = []
    for line in data:
        coordinates = [
            Coordinate([int(number) for number in coordinate.split(",")])
            for coordinate in line.split(" -> ")
        ]
        for start, end in zip(coordinates[:-1], coordinates[1:]):
            line_segments += [LineSegment(start, end)]
    return line_segments


def part1(data):
    """Advent of code 2022 day 14 - Part 1"""
    answer = 0
    line_segments = build_line_segments(data)
    print(line_segments)

    print(f"Solution day 14, part 1: {answer}")
    return answer


def part2(data):
    """Advent of code 2022 day 14 - Part 2"""
    answer = 0

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
    # test_data = False
    test_data = True
    submit_answer = False
    # submit_answer = True
    main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    # main("ab", should_submit=submit_answer, load_test_data=test_data)
