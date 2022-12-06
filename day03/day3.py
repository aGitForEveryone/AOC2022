from aocd import get_data, submit


def parse_data() -> list[str]:
    """Parser function to parse today's data"""
    data = get_data(day=3, year=2022)
    # with open("input3.1", "r") as f:
    #     data = f.read()
    lines = data.splitlines()
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return lines


def split_rucksacks(data: list[str]) -> list[list[str]]:
    """Split the contents of each rucksack in two, identifies the contents of
    each compartment in a rucksack"""
    split_contents = [
        [
            rucksack_content[: (idx_middle := len(rucksack_content) // 2)],
            rucksack_content[idx_middle:],
        ]
        for rucksack_content in data
    ]
    return split_contents


def find_common_items(*groups: str) -> set[str]:
    """Find the items that two compartments have in common"""
    if not groups:
        raise ValueError(f"No groups were given to check common items between.")
    common_items = set.intersection(*[set(group) for group in groups])

    return common_items


def get_item_priority(item: str) -> int:
    """Find the priority of the given item. `a` through `z` have priority 1
    through 26, `A` through `Z` have priority 27 through 52"""
    if len(item) > 1:
        raise ValueError(
            f"Multiple items given, while the function expects 1 "
            f"item. (Items received: {item}"
        )

    if item.isupper():
        priority = ord(item) - ord("A") + 27
    elif item.islower():
        priority = ord(item) - ord("a") + 1
    else:
        raise ValueError(
            f"Expected to receive a letter [a-zA-Z], but got "
            f"something else: '{item}'"
        )
    return priority


def part1(data: list[str]) -> int:
    """Advent of code 2022 day 3 - Part 1
    Find the common items between the two compartments of each rucksack, then
    find the priorities of the common items. The final answer is the sum of all
    the priorities."""
    answer = 0
    split_contents = split_rucksacks(data)
    for rucksack in split_contents:
        common_items = find_common_items(rucksack[0], rucksack[1])
        answer += sum([get_item_priority(item) for item in common_items])

    print(f"Solution day 3, part 1: {answer}")
    return answer


def part2(data: list[str]) -> int:
    """Advent of code 2022 day 3 - Part 2
    Find the common item in each group of three rucksacks (not caring about
    which compartment the item is in). Then find the priority of this common
    item and sum that over all rucksacks."""
    answer = 0
    for start_group_idx in range(0, len(data), 3):
        common_items = find_common_items(*data[start_group_idx : start_group_idx + 3])
        answer += sum([get_item_priority(item) for item in common_items])

    print(f"Solution day 3, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
    """
    data = parse_data()

    for part in parts:
        if part == "a":
            aocd_result = part1(data)
        elif part == "b":
            aocd_result = part2(data)
        else:
            raise ValueError(f"Wrong part chosen, expecting 'a' or 'b': got {part}")

        if should_submit:
            submit(aocd_result, part=part, day=3, year=2022)


if __name__ == "__main__":
    submit_answer = False
    # submit_answer = True
    # main("a", submit_answer)
    # main("b", submit_answer)
    main("ab", submit_answer)
