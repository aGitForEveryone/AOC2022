import functools
from enum import Enum
from typing import Union

from aocd import get_data, submit


class Order(Enum):
    CORRECT = -1
    INDECISIVE = 0
    INCORRECT = 1


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


def int_int_compare(left: int, right: int) -> Order:
    """Compare two ints"""
    if left == right:
        return Order.INDECISIVE
    elif left < right:
        return Order.CORRECT
    else:  # right > left
        return Order.INCORRECT


def compare_list_items(left: Union[list, int], right: Union[list, int]) -> Order:
    """Compare two items. If both are int we can do a direct comparison,
    otherwise we should compare left and right as lists (converting either into
    a list if they are of type int) - This recursively calls the compare list
    function again"""
    if isinstance(left, int) and isinstance(right, int):
        status = int_int_compare(left, right)
    else:
        # If either left or right is an int, we make it into a list and then
        # compare two lists
        if isinstance(left, int):
            left = [left]
        if isinstance(right, int):
            right = [right]
        status = lists_in_right_order(left, right)
    return status


def lists_in_right_order(left: list, right: list) -> Order:
    """Check if lists left and right are in the correct order"""
    for left_item, right_item in zip(left, right):
        status = compare_list_items(left_item, right_item)
        if status != Order.INDECISIVE:
            return status
    else:
        # If we reached the end of the for-loop, then we should check which list
        # ran out of items first
        return int_int_compare(len(left), len(right))


def process_pairs(pairs: list[str]) -> list[int]:
    """Compare the lists in each pair and return the index of the pairs that
    are in the correct order"""
    idx_correctly_ordered_pairs = []
    for idx, pair in enumerate(pairs):
        left, right = tuple(map(eval, pair.split()))
        status = lists_in_right_order(left, right)
        if status == Order.CORRECT:
            idx_correctly_ordered_pairs += [idx]
    return idx_correctly_ordered_pairs


def part1(data: list[str]) -> int:
    """Advent of code 2022 day 13 - Part 1"""
    correctly_ordered_pairs = process_pairs(data)
    answer = sum(correctly_ordered_pairs) + len(correctly_ordered_pairs)

    print(f"Solution day 13, part 1: {answer}")
    return answer


def lists_in_right_order_int(left: list, right: list) -> int:
    """Extracts the int value from the enum entry, since the compare function
    needs an int"""
    return lists_in_right_order(left, right).value


def sort_all_packets(packets: list[list]) -> list[list]:
    """Sort all the packets in ascending order according to the established
    list comparison rules. Uses the built-in sorted function with custom compare
    function.

    Since we can only compare elements relative to each other to sort the list,
    we utilize functools.cmp_to_key to make our custom compare function work
    with the key parameter of sorted."""
    return sorted(packets, key=functools.cmp_to_key(lists_in_right_order_int))


def part2(data: list[str]) -> int:
    """Advent of code 2022 day 13 - Part 2"""
    # concatenate the data again so that every packet is on a separate line,
    # then split the lines to get the individual packets, then convert the
    # packets to lists using eval.
    data = list(map(eval, "\n".join(data).splitlines()))
    sorted_packets = sort_all_packets(data)

    # Add the first divider package
    divider_packet_1 = [[2]]
    for idx, packet in enumerate(sorted_packets):
        if lists_in_right_order(divider_packet_1, packet) == Order.CORRECT:
            divider_1_idx = idx
            sorted_packets.insert(idx, divider_packet_1)
            break
    else:
        # if we are at the end of the list, then the packets should be appended
        # to the end
        divider_1_idx = len(sorted_packets)

    # Starting from where the first divider packet was inserted, find the spot
    # to insert the second divider packet (which is larger than the first)
    divider_packet_2 = [[6]]
    for idx, packet in enumerate(sorted_packets[divider_1_idx + 1 :]):
        if lists_in_right_order(divider_packet_2, packet) == Order.CORRECT:
            # idx counts from start of slice and not from the start of the
            # sorted list, so we need to correct the value.
            divider_2_idx = idx + divider_1_idx + 1
            sorted_packets.insert(idx + divider_1_idx + 1, divider_packet_2)
            break
    else:
        # if we are at the end of the list, then the packets should be appended
        # to the end
        divider_2_idx = len(sorted_packets)

    answer = (divider_1_idx + 1) * (divider_2_idx + 1)

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
    test_data = False
    # test_data = True
    submit_answer = False
    # submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    main("ab", should_submit=submit_answer, load_test_data=test_data)
