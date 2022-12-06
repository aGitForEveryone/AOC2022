import pprint
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
        with open("input5.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=5, year=2022)

    stack, instructions = data.split("\n\n")
    instructions = re.findall("move (\d+) from (\d+) to (\d+)", instructions)
    instructions = [
        tuple(int(number) for number in instruction) for instruction in instructions
    ]
    # instructions = instructions.splitlines()
    # stack = stack.replace("] [", " ").replace("]", "").replace("[", "").splitlines()
    # Take the length of the bottom row of the stack, because that should
    # definitely all be filled, i.e. assuming no empty stacks in the input.
    parsed_stacks = [
        "GBDCPR",
        "GVH",
        "MPJDQSN",
        "MNCDGLSP",
        "SLFPCNBJ",
        "STGVZDBQ",
        "QTFHMZB",
        "FBDMC",
        "GQCF",
    ]
    if load_test_data:
        parsed_stacks = ["NZ", "DCM", "P"]
    # for stack_idx in range(len(stack[-2])):
    #     new_stack = ""
    #     # from each line of the input stack, fetch the character at location
    #     # stack_idx and append it to the new_stack
    #     for line in stack[:-1]:
    #         new_stack += line[stack_idx]
    #     parsed_stacks += [new_stack.strip()]
    # lines = data.splitlines()
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return {"stacks": parsed_stacks, "instructions": instructions}


def part1(data):
    """Advent of code 2022 day 5 - Part 1"""
    stacks = data["stacks"].copy()
    for (num_to_move, source_stack, target_stack) in data["instructions"]:
        if len(stacks[source_stack - 1]) < num_to_move:
            raise ValueError(f'stack not long enough. Wanted to move: {num_to_move} but source stack is only {len(stacks[source_stack - 1])} long')
        items_to_move = stacks[source_stack - 1][:num_to_move][::-1]
        stacks[source_stack - 1] = stacks[source_stack - 1][num_to_move:]
        stacks[target_stack - 1] = items_to_move + stacks[target_stack - 1]

    answer = ""
    for stack in stacks:
        answer += stack[0]
    print(f"Solution day 5, part 1: {answer}")
    return answer


def part2(data):
    """Advent of code 2022 day 5 - Part 2"""
    stacks = data["stacks"].copy()
    for (num_to_move, source_stack, target_stack) in data["instructions"]:
        if len(stacks[source_stack - 1]) < num_to_move:
            raise ValueError(f'stack not long enough. Wanted to move: {num_to_move} but source stack is only {len(stacks[source_stack - 1])} long')
        items_to_move = stacks[source_stack - 1][:num_to_move]
        stacks[source_stack - 1] = stacks[source_stack - 1][num_to_move:]
        stacks[target_stack - 1] = items_to_move + stacks[target_stack - 1]

    answer = ""
    for stack in stacks:
        answer += stack[0]

    print(f"Solution day 5, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input5.1'
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
            submit(aocd_result, part=part, day=5, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    # submit_answer = False
    submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    main("b", should_submit=submit_answer, load_test_data=test_data)
    # main("ab", should_submit=submit_answer, load_test_data=test_data)
