import re

from aocd import get_data, submit
import numpy as np

data = get_data(day=13, year=2022)
lines = data.splitlines()
numbers = [int(x) for x in re.findall("(-?\d+)", data)]


def part1():
    """Advent of code 2022 day 13 - Part 1"""
    answer = 0

    print(f"Solution day 13, part 1: {answer}")
    return answer


def part2():
    """Advent of code 2022 day 13 - Part 2"""
    answer = 0

    print(f"Solution day 13, part 2: {answer}")
    return answer


if __name__ == "__main__":
    part = "a"
    # part = "b"
    submit_answer = False

    aocd_result = part1() if part == "a" else part2()
    if submit_answer:
        submit(aocd_result, part=part, day=13, year=2022)
