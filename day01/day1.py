from aocd import get_data, submit


def parse_data() -> list[list[int]]:
    """The data contains the total calories for the collection of foods that
    each elf holds. The inventory of each elf is separated by double newlines
    and within each elf's inventory, the number of calories for each food is
    separated by a single new line. An example of a data input is:
    ```
    1000
    2000
    3000

    4000

    5000
    6000
    ```
    Here we see the inventories of 3 elves: elf 1 holding three foods having
    1000, 2000, and 3000 calories respectively, elf 2 holding 1 food with 4000
    calories, and finally elf 3 holding 2 foods with 5000 and 6000 calories
    respectively.

    Each line in the data is the number of calories that each food contains.
    The food inventory of the different elves is separated by n

    Returns:
        List of lists where each inner list represents the inventory of 1 elf.
        For the above example, this function returns
        ```
        [[1000, 2000, 3000], [4000], [5000, 6000]]
        ```
    """
    data = get_data(day=1, year=2022)
    elf_data = data.split("\n\n")
    total_calories_per_elf = [
        [int(calories_per_snack) for calories_per_snack in elf.splitlines()]
        for elf in elf_data
    ]
    # lines = data.splitlines()
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return total_calories_per_elf


def sum_calories(data: list[list[int]]) -> list[int]:
    """Sums the calories of each food item in each elf's inventory"""
    return [sum(inventory) for inventory in data]


def part1(data: list[list[int]]) -> int:
    """Advent of code 2022 day 1 - Part 1
    Find the inventory carrying the largest amount of calories
    """
    answer = max(sum_calories(data))
    print(f"Solution day 1, part 1: {answer}")
    return answer


def part2(data: list[list[int]]) -> int:
    """Advent of code 2022 day 1 - Part 2
    Find the sum of the top three inventories carrying the most calories
    """
    answer = sum(sorted(sum_calories(data), reverse=True)[:3])
    print(f"Solution day 1, part 2: {answer}")
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
            submit(aocd_result, part=part, day=1, year=2022)


if __name__ == "__main__":
    submit_answer = False
    # main("a", submit_answer)
    # main("b", submit_answer)
    main("ab", submit_answer)
