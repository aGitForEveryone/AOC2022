import re
from typing import Union

from aocd import get_data, submit
import numpy as np

import helper_functions


def parse_data(load_test_data: bool = False) -> list[str]:
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local
                            directory
    """
    if load_test_data:
        with open("input13.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=13, year=2022)
    data = data.split("\n\n")
    # lines = data.splitlines()
    # grid = np.array(helper_functions.digits_to_int(data.splitlines()))
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return data


def int_int_compare(left: int, right: int) -> bool:
    """Compare two ints"""
    if left == right:
        return 0


def compare_list_items(left: Union[list, int], right: Union[list, int]):
    """Compare two items"""
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        elif left > right:
            return False
        # when left_item == right_item, continue


def lists_in_right_order(left: list, right: list) -> bool:
    """Check if the lists are in the correct order"""
    for left_item, right_item in zip(left, right):
        result = compare_list_items(left_item, right_item)


def process_pairs(pairs: list[str]):
    """Compare the lists in each pair"""
    for pair in pairs:
        left, right = tuple(map(lambda packet: eval(packet), pair.split()))


def part1(data: list[str]) -> int:
    """Advent of code 2022 day 13 - Part 1"""
    answer = 0
    print(data)

    print(f"Solution day 13, part 1: {answer}")
    return answer


def part2(data):
    """Advent of code 2022 day 13 - Part 2"""
    answer = 0

    print(f"Solution day 13, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input13.1'
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
            submit(aocd_result, part=part, day=13, year=2022)


if __name__ == "__main__":
    # test_data = False
    test_data = True
    submit_answer = False
    # submit_answer = True
    main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    # main("ab", should_submit=submit_answer, load_test_data=test_data)
