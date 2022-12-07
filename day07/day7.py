import re
from pathlib import Path

from aocd import get_data, submit
import numpy as np
import anytree
from anytree import AnyNode


HOME = 'aoc2022day7'
DISK_SIZE = 70_000_000


def parse_data(load_test_data: bool = False) -> list[str]:
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local
                            directory
    """
    if load_test_data:
        with open("input7.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=7, year=2022)
    lines = data.splitlines()
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return lines


def create_file_system(cd_ls_output: list[str]) -> dict[Path, AnyNode]:
    """Parse the output given by a series of cd and ls commands and create a
    file system based on it"""
    # Start at the home directory
    current_directory = Path(HOME)
    file_system = {
        current_directory: AnyNode(name=str(current_directory), size=None,
                                   is_dir=True)
    }
    for line in cd_ls_output:
        # print(f'{line = }')
        match line.split():
            case ['$', 'cd', '/']:
                # print(f'Navigating to home')
                current_directory = Path(HOME)
                # print(f'{current_directory = }')
            case ['$', 'cd', '..']:
                # print(f'Navigating to parent')
                current_directory = current_directory.parent
                # print(f'{current_directory = }')
            case ['$', 'cd', target_directory]:
                # print(f'Navigating to {target_directory}')
                current_directory = current_directory / target_directory
                # print(f'{current_directory = }')
            case ['$', 'ls']:
                pass
            case ['dir', directory_name]:
                new_directory_path = current_directory / directory_name
                if new_directory_path not in file_system:
                    file_system[new_directory_path] = AnyNode(name=f'{directory_name}/',
                                                              size=None,
                                                              is_dir=True,
                                                              parent=file_system[current_directory])
            case [file_size, file_name]:
                new_file_path = current_directory / file_name
                if new_file_path not in file_system:
                    file_system[new_file_path] = AnyNode(name=f'{file_name} ({int(file_size):_})',
                                                         size=int(file_size),
                                                         is_dir=False,
                                                         parent=file_system[current_directory])

    return file_system


def render_file_system(root_node: AnyNode) -> None:
    """Pretty print the filesystem starting at the given root node"""
    for pre, _, node in anytree.RenderTree(root_node):
        print(f'{pre}{node.name}')


def calculate_directory_size(dir_node: AnyNode) -> None:
    """Calculate the size of the given directory node. If sub-directories exist,
    then the function will recursively calculate the size of those directories
    as well. The size of the nodes is added in-place. Also updates the name of
    the node to display the directory size."""
    dir_size = 0
    for child_node in dir_node.children:
        if child_node.is_dir and not child_node.size:
            # then we haven't calculated the size of the directory yet.
            # Calculate the size and add it inplace in the node information.
            calculate_directory_size(child_node)
        dir_size += child_node.size
    dir_node.size = dir_size
    dir_node.name = f'{dir_node.name} ({dir_node.size:_})'


def find_size_sum_directories_with_size_less_than(max_size: int, root_node: AnyNode) -> int:
    """Sum the sizes of the directories with size less than given max_size"""
    sum = 0
    for _, __, node in anytree.RenderTree(root_node):
        if node.is_dir and node.size <= max_size:
            sum += node.size
    return sum


def prepare_file_system(data: list[str]) -> tuple[dict[Path, AnyNode], AnyNode]:
    """Create file system from cd-ls output and calculate directory sizes"""
    file_system = create_file_system(data)
    root_node = file_system[Path(HOME)]
    calculate_directory_size(root_node)

    return file_system, root_node


def part1(data: tuple[dict[Path, AnyNode], AnyNode]) -> int:
    """Advent of code 2022 day 7 - Part 1"""
    _, root_node = data

    answer = find_size_sum_directories_with_size_less_than(100_000, root_node)
    print(f"Solution day 7, part 1: {answer}")
    return answer


def find_size_smallest_directory_above(dir_size: int, root_node: AnyNode) -> int:
    """Find the size of the directory that is the closest above the given
    dir_size within the given file_system (starting at root_node)"""
    smallest_target = DISK_SIZE
    for _, __, node in anytree.RenderTree(root_node):
        if node.is_dir and smallest_target > node.size >= dir_size:
            smallest_target = node.size
    return smallest_target


def part2(data: tuple[dict[Path, AnyNode], AnyNode]) -> int:
    """Advent of code 2022 day 7 - Part 2"""
    _, root_node = data
    free_space = DISK_SIZE - root_node.size
    space_to_free_for_update = 30_000_000 - free_space
    smallest_directory_size = find_size_smallest_directory_above(
        space_to_free_for_update, root_node
    )

    answer = smallest_directory_size

    print(f"Solution day 7, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input7.1'
    """
    data = parse_data(load_test_data=load_test_data)
    data = prepare_file_system(data)

    for part in parts:
        if part == "a":
            aocd_result = part1(data)
        elif part == "b":
            aocd_result = part2(data)
        else:
            raise ValueError(f"Wrong part chosen, expecting 'a' or 'b': got {part}")

        if should_submit:
            submit(aocd_result, part=part, day=7, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    submit_answer = False
    # submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    main("b", should_submit=submit_answer, load_test_data=test_data)
    # main("ab", should_submit=submit_answer, load_test_data=test_data)
