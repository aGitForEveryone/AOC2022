import re
from typing import Callable

from aocd import get_data, submit


ELF_RANGE = tuple[int, int]


def parse_data(load_test_data: bool = False) -> list[ELF_RANGE]:
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local
                            directory
    """
    if load_test_data:
        with open("input4.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=4, year=2022)
    cleaning_ranges: list[ELF_RANGE] = re.findall("(\d+)-(\d+)", data)
    int_data = [
        tuple(int(number) for number in cleaning_range)
        for cleaning_range in cleaning_ranges
    ]
    # lines = data.splitlines()
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return int_data


def is_range_fully_contained(self: ELF_RANGE, other: ELF_RANGE) -> bool:
    """Check if range self is fully contained in the other range.
    This is true if
        start of self >= start of other
        and
        end of self <= end of other
    """
    return self[0] >= other[0] and self[1] <= other[1]


def is_overlapping(self: ELF_RANGE, other: ELF_RANGE) -> bool:
    """Check if there is any overlap between self and other.
    To find whether a range is overlapping, we check if self is not fully
    outside of other. That is, if the start of self is larger than the end of
    other, or the end of self is smaller than the start of other is not True.
    So, we are essentially reversing the question, as this takes fewer checks to
    verify."""
    # Positive check: check if self is overlapping
    # return other[0] <= self[0] <= other[1] or other[0] <= self[1] <= other[1]

    # Reversed check: check if self is outside other
    return not (self[0] > other[1] or self[1] < other[0])


def find_ranges_of_interest(
    data: list[ELF_RANGE],
    valid_range_check: Callable,
) -> list[list[ELF_RANGE, ELF_RANGE]]:
    """Select pairs defined valid by the valid_range_check function.
    valid_range_check should take 2 inputs of type ELF_RANGE and return a
    boolean indicating the range pairs should be selected."""
    valid_ranges = []
    for pair_start_idx in range(0, len(data), 2):
        range1 = data[pair_start_idx]
        range2 = data[pair_start_idx + 1]
        if valid_range_check(range1, range2) or valid_range_check(range2, range1):
            valid_ranges += [[range1, range2]]

    return valid_ranges


def part1(data: list[ELF_RANGE]) -> int:
    """Advent of code 2022 day 4 - Part 1
    Find number of pairs where one elf cleaning range is fully contained in the
    other"""
    pairs_with_completely_contained_ranges = find_ranges_of_interest(
        data, is_range_fully_contained
    )
    answer = len(pairs_with_completely_contained_ranges)

    print(f"Solution day 4, part 1: {answer}")
    return answer


def part2(data: list[ELF_RANGE]):
    """Advent of code 2022 day 4 - Part 2
    Find number of pairs where there is some overlap between elf's cleaning
    ranges"""
    pairs_with_overlap = find_ranges_of_interest(data, is_overlapping)
    answer = len(pairs_with_overlap)

    print(f"Solution day 4, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input4.1'
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
            submit(aocd_result, part=part, day=4, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    submit_answer = False
    # submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    main("ab", should_submit=submit_answer, load_test_data=test_data)
