import re
from typing import Callable, Self

from aocd import get_data, submit
import numpy as np

import helper_functions


class Monkey:
    largest_worry_level = None

    def __init__(
        self,
        item_list: list[int],
        update_worry_level: Callable,
        test_worry_level: Callable,
    ):
        """

        Args:
            item_list:              List of starting items each monkey has. The
                                    value of the item is the current worry level
                                    for the item.
            update_worry_level:     Callable that returns a new worry level
                                    (int), reflecting how the worry level
                                    changes when this monkey inspects an item
            test_worry_level:       Callable that takes a worry level and
                                    returns a boolean that will decide to which
                                    monkey the item gets thrown.
            largest_worry_level:    Largest worry level to consider, everything
                                    above can be reduced
        """
        self.item_list = item_list
        self.update_worry_level = update_worry_level
        self.test_worry_level = test_worry_level
        # Target monkeys cannot be set during initialization since, target
        # monkeys potentially do not exist yet
        self.target_monkeys = None
        self._number_of_items_inspected = 0

    def set_target_monkeys(self, target_monkeys: dict[bool, Self]) -> None:
        """Set monkeys to throw items to depending on the result of
        test_worry_level."""
        self.target_monkeys = target_monkeys

    def do_turn(self) -> None:
        """Perform turn. For all items in self.item_list:
            - Inspect item and update worry level
            - Test item worry level and throw item to next monkey
        At the end of the turn update the number of items this monkey inspected
        and clean the item list (as all items will be thrown to other monkeys).
        """
        for item_worry_level in self.item_list:
            new_worry_level = self._inspect_item(item_worry_level)
            self._throw_item(new_worry_level)
        self._number_of_items_inspected += len(self.item_list)
        self.item_list = []

    def _inspect_item(self, item_worry_level: int) -> int:
        """Return the new worry level after the monkey inspected the item. After
        the monkeys' worry level update function is called, it is checked if the
        item is damaged or not.
        If not damaged, the worry level is divided by 3
        and rounded down to the nearest integer."""
        new_worry_level = self.update_worry_level(item_worry_level)
        if new_worry_level > self.largest_worry_level:
            new_worry_level %= self.largest_worry_level
        return new_worry_level

    def _throw_item(self, item_worry_level: int) -> None:
        """Throw the item to the next monkey"""
        if not self.target_monkeys:
            raise ValueError(
                f"Target monkeys have not yet been set. Please set"
                f" the target monkeys first using a call to "
                f"Monkey.set_target_monkeys(target_monkeys)."
            )
        target_monkey = self.target_monkeys[self.test_worry_level(item_worry_level)]
        target_monkey.receive_item(item_worry_level)

    def receive_item(self, item_worry_level: int) -> None:
        """Receives incoming item and add it to the monkeys' item list"""
        self.item_list += [item_worry_level]

    def set_activity_level(self, activity_level: int) -> None:
        """Overwrite the activity level"""
        self._number_of_items_inspected = activity_level

    @property
    def activity_level(self) -> int:
        """Returns activity level for the monkey"""
        return self._number_of_items_inspected


def parse_monkeys(data: list[str], divide_worry_by: int = 3) -> list[Monkey]:
    """Read monkey configuration, an example input configuration is:
    Monkey 2:
        Starting items: 79, 60, 97
        Operation: new = old * old
        Test: divisible by 13
            If true: throw to monkey 1
            If false: throw to monkey 3
    """
    target_monkeys = []
    monkeys = []
    largest_worry_level = 1
    if not divide_worry_by:
        divide_worry_by = 1
    for monkey in data:
        monkey_data = monkey.splitlines()
        # print(f'{monkey_data = }')

        starting_items = helper_functions.digits_to_int(
            re.findall("-?\d+", monkey_data[1]), individual_character=False
        )

        # print(f'Operation: "{monkey_data[2].split("= ")[1]}"')
        worry_updater = lambda old, operation=(monkey_data[2].split("= ")[1]): eval(operation) // divide_worry_by

        modulus_value = helper_functions.digits_to_int(
            re.findall("-?\d+", monkey_data[3]), individual_character=False
        )[0]
        largest_worry_level *= modulus_value
        test_worry_level = lambda worry_level, value=modulus_value: (worry_level % value) == 0

        target_monkey_true = helper_functions.digits_to_int(
            re.findall("-?\d+", monkey_data[4]), individual_character=False
        )[0]
        target_monkey_false = helper_functions.digits_to_int(
            re.findall("-?\d+", monkey_data[5]), individual_character=False
        )[0]
        target_monkeys += [{True: target_monkey_true, False: target_monkey_false}]

        monkeys += [
            Monkey(
                starting_items,
                update_worry_level=worry_updater,
                test_worry_level=test_worry_level,
            )
        ]
    # convert the target monkey numbers into monkey object references
    for targets, monkey in zip(target_monkeys, monkeys):
        monkey.set_target_monkeys(
            {True: monkeys[targets[True]], False: monkeys[targets[False]]}
        )
    Monkey.largest_worry_level = largest_worry_level
    return monkeys


def parse_data(load_test_data: bool = False) -> list[Monkey]:
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local
                            directory
    """
    if load_test_data:
        with open("input11.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=11, year=2022)
    data = data.split("\n\n")
    # lines = data.splitlines()
    # grid = np.array(helper_functions.digits_to_int(data.splitlines()))
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return data


def perform_round(monkeys: list[Monkey]) -> None:
    """Perform a turn for each monkey"""
    for monkey in monkeys:
        monkey.do_turn()


def get_state_item_lists(monkeys: list[Monkey]) -> tuple[tuple[int]]:
    """"""
    return tuple(tuple(monkey.item_list) for monkey in monkeys)


def do_number_of_rounds(monkeys: list[Monkey], number_of_rounds: int, cache: set) -> int:
    """"""
    for round_number in range(number_of_rounds):
        if round_number % 100:
            print(f'Starting round {round_number}')
        perform_round(monkeys)
        current_item_list_state = get_state_item_lists(monkeys)
        if current_item_list_state not in cache:
            cache.add(current_item_list_state)
        else:
            print(f'Loop found at the end of round {round_number}! Extrapolating to end.')
            number_loops_in_total_rounds = number_of_rounds // (round_number + 1)
            for monkey in monkeys:
                monkey.set_activity_level(monkey.activity_level * number_loops_in_total_rounds)
            # Calculate how many rounds still need to played and exit
            return number_of_rounds - number_loops_in_total_rounds * (round_number + 1)

    return 0


def part1(data: list[str]) -> int:
    """Advent of code 2022 day 11 - Part 1"""
    monkeys = parse_monkeys(data, divide_worry_by=3)
    number_of_rounds = 20
    for round_number in range(number_of_rounds):
        perform_round(monkeys)
    # cache_item_list = {get_state_item_lists(monkeys)}
    # remaining_rounds = do_number_of_rounds(monkeys, number_of_rounds, cache_item_list)
    # _ = do_number_of_rounds(monkeys, remaining_rounds, set())

    number_interactions = sorted([monkey.activity_level for monkey in monkeys])
    answer = number_interactions[-1] * number_interactions[-2]

    print(f"Solution day 11, part 1: {answer}")
    return answer


def part2(data: list[str]) -> int:
    """Advent of code 2022 day 11 - Part 2"""
    monkeys = parse_monkeys(data, divide_worry_by=1)
    number_of_rounds = 10_000
    for round_number in range(number_of_rounds):
        perform_round(monkeys)
    # cache_item_list = {get_state_item_lists(monkeys)}
    # remaining_rounds = do_number_of_rounds(monkeys, number_of_rounds, cache_item_list)
    # _ = do_number_of_rounds(monkeys, remaining_rounds, set())

    number_interactions = sorted([monkey.activity_level for monkey in monkeys])
    answer = number_interactions[-1] * number_interactions[-2]

    print(f"Solution day 11, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input11.1'
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
            submit(aocd_result, part=part, day=11, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    # submit_answer = False
    submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    main("b", should_submit=submit_answer, load_test_data=test_data)
    # main("ab", should_submit=submit_answer, load_test_data=test_data)
