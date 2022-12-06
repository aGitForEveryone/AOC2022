import re
from typing import TypedDict

from aocd import get_data, submit


STACKS = list[str]
INSTRUCTIONS = list[tuple[int]]


class StacksAndInstructions(TypedDict):
    stacks: STACKS
    instructions: INSTRUCTIONS


def parse_data(load_test_data: bool = False) -> StacksAndInstructions:
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

    stacks, instructions = data.split("\n\n")
    instructions = re.findall("move (\d+) from (\d+) to (\d+)", instructions)
    instructions = [
        tuple(int(number) for number in instruction) for instruction in instructions
    ]

    # The input passes the stacks in a vertical manner like:
    #     [D]
    # [N] [C]
    # [Z] [M] [P]
    #  1   2   3
    # This makes parsing the input quite complex. We make our life easier by
    # transposing the string matrix. This will put the contents of the stack on
    # one single line instead. Above stack input transposes to:
    # [(' ', '[', '[', ' '),
    #  (' ', 'N', 'Z', '1'),
    #  (' ', ']', ']', ' '),
    #  (' ', ' ', ' ', ' '),
    #  ('[', '[', '[', ' '),
    #  ('D', 'C', 'M', '2'),
    #  (']', ']', ']', ' '),
    #  (' ', ' ', ' ', ' '),
    #  (' ', ' ', '[', ' '),
    #  (' ', ' ', 'P', '3'),
    #  (' ', ' ', ']', ' ')]
    # Now it's just a matter of identifying which lines contain the stacks and
    # create strings from the tuples. The desired output for above example is:
    # ['NZ', 'DCM', 'P']
    # In this code, the stacks are identified by the lines that:
    #   - have a digit as last character in the tuple
    #   and
    #   - have a letter as second to last character in tuple (uppercase or lowercase)
    # With this method we can parse inputs with 10 or more stacks.
    # ASSUMPTIONS:
    #   1. All stacks in the input contain at least 1 item
    #   2. Items are represented by 1 letter each (both uppercase and lowercase is allowed)
    #   3. Stack items are aligned in the same column and are aligned above a
    #      digit, that represents the stack index. For stacks with index >= 10
    #      the stack items can be aligned above any of the two digits, but the
    #      items should all be in the same column.
    # Any vertical stack that doesn't follow above assumptions will not be
    # detected.
    transposed_stacks = list(zip(*stacks.splitlines()))
    actual_stacks = [
        line[:-1]
        for line in transposed_stacks
        if (line[-1].isdigit() and line[-2].isalpha())
    ]
    parsed_stacks = ["".join(stack).strip() for stack in actual_stacks]

    # lines = data.splitlines()
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return {"stacks": parsed_stacks, "instructions": instructions}


def get_top_of_stacks(stacks: STACKS) -> str:
    """Get the top item of each stack, concatenated in a single string. The
    order in the string is the same as the stack order in stacks."""
    stack_string = ""
    for stack in stacks:
        if not stack:
            # In case the stack is empty, we add a space to the output string.
            stack_string += ' '
        else:
            stack_string += stack[0]
    return stack_string


def part1(data: StacksAndInstructions) -> str:
    """Advent of code 2022 day 5 - Part 1"""
    # Because we will change the stacks inplace, we make a copy of the list so
    # we don't change the original list.
    stacks = data["stacks"].copy()
    for (num_to_move, source_stack, target_stack) in data["instructions"]:
        if len(stacks[source_stack - 1]) < num_to_move:
            raise ValueError(
                f"stack not long enough. Wanted to move: {num_to_move} but "
                f"source stack is only {len(stacks[source_stack - 1])} long."
            )
        items_to_move = stacks[source_stack - 1][:num_to_move][::-1]
        stacks[source_stack - 1] = stacks[source_stack - 1][num_to_move:]
        stacks[target_stack - 1] = items_to_move + stacks[target_stack - 1]

    answer = get_top_of_stacks(stacks)
    print(f"Solution day 5, part 1: {answer}")
    return answer


def part2(data: StacksAndInstructions) -> str:
    """Advent of code 2022 day 5 - Part 2"""
    # Because we will change the stacks inplace, we make a copy of the list so
    # we don't change the original list.
    stacks = data["stacks"].copy()
    for (num_to_move, source_stack, target_stack) in data["instructions"]:
        if len(stacks[source_stack - 1]) < num_to_move:
            raise ValueError(
                f"stack not long enough. Wanted to move: {num_to_move} but "
                f"source stack is only {len(stacks[source_stack - 1])} long."
            )
        items_to_move = stacks[source_stack - 1][:num_to_move]
        stacks[source_stack - 1] = stacks[source_stack - 1][num_to_move:]
        stacks[target_stack - 1] = items_to_move + stacks[target_stack - 1]

    answer = get_top_of_stacks(stacks)

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
    submit_answer = False
    # submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    main("ab", should_submit=submit_answer, load_test_data=test_data)
