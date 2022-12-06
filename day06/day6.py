import re

from aocd import get_data, submit
import numpy as np


def parse_data(load_test_data: bool = False):
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local 
                            directory
    """
    if load_test_data:
        with open("input6.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=6, year=2022)
    # lines = data.splitlines()
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return data


def find_end_of_start_packet(message: str, num_distinct_characters: int = 4) -> int:
    """Find the index of the end of the start indicator of the message. The
    start indicator is the first 4 consecutive characters that are all different
    """
    target_index = num_distinct_characters - 1
    while len(set(message[target_index - (num_distinct_characters - 1): target_index + 1])) < num_distinct_characters:
        target_index += 1
        if target_index == len(message):
            raise ValueError(f'Reached end of string without finding the start'
                             f'package')
    return target_index


def part1(data):
    """Advent of code 2022 day 6 - Part 1"""
    answer = find_end_of_start_packet(data) + 1
    print(data)

    print(f"Solution day 6, part 1: {answer}")
    return answer


def part2(data):
    """Advent of code 2022 day 6 - Part 2"""
    answer = find_end_of_start_packet(data, 14) + 1

    print(f"Solution day 6, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer. 

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file 
                        called 'input6.1'
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
            submit(aocd_result, part=part, day=6, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    # submit_answer = False
    submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    main("b", should_submit=submit_answer, load_test_data=test_data)
    # main("ab", should_submit=submit_answer, load_test_data=test_data)
