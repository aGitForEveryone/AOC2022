import re
from enum import Enum

from aocd import get_data, submit
import numpy as np

import helper_functions


def parse_data(load_test_data: bool = False) -> np.ndarray:
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local
                            directory
    """
    if load_test_data:
        with open("input8.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=8, year=2022)
    lines = data.splitlines()
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return helper_functions.pad_numpy_array(
        np.array(helper_functions.digits_to_int(lines)), -1
    )


def check_visibility(grid: np.ndarray, visibility_grid: np.ndarray) -> None:
    """Fill the visibility grid inplace with ones where trees are visible from
    the outside"""
    num_rows, num_cols = grid.shape
    for row in range(1, num_rows):
        highest_tree_left = -1
        highest_tree_right = -1
        for col in range(1, num_cols):
            # left
            if grid[row, col] > highest_tree_left:
                visibility_grid[row, col] = 1
                highest_tree_left = grid[row, col]

            # right
            if grid[row, num_cols - col - 1] > highest_tree_right:
                visibility_grid[row, num_cols - col - 1] = 1
                highest_tree_right = grid[row, num_cols - col - 1]

    for col in range(1, num_cols):
        highest_tree_top = -1
        highest_tree_bottom = -1
        for row in range(1, num_rows):
            # top
            if grid[row, col] > highest_tree_top:
                visibility_grid[row, col] = 1
                highest_tree_top = grid[row, col]

            # bottom
            if grid[num_rows - row - 1, col] > highest_tree_bottom:
                visibility_grid[num_rows - row - 1, col] = 1
                highest_tree_bottom = grid[num_rows - row - 1, col]


class Direction(Enum):
    LEFT = (0, -1)
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)


def scan_along_direction(
    grid: np.ndarray,
    home_location: tuple[int, int],
    direction: Direction,
    ignore_outer_edges: bool = False,
) -> int:
    """Scans from a given point in a grid to the edge along a given direction"""
    scenic_score = 0
    distance = 1
    num_rows, num_cols = grid.shape
    # Here we use a little trick that boolean are converted to 0 and 1 during
    # arithmetic or during comparisons with numbers. For example, if the grid
    # is 7x7 and ignore_outer_edges is True, the comparison below becomes
    #   1 <= new_location <= 5
    # if ignore_outer_edges is False, the comparison becomes:
    #   0 <= new_location <= 6
    while (
        ignore_outer_edges
        <= (new_row := home_location[0] + distance * direction.value[0])
        <= num_rows - 1 - ignore_outer_edges
    ) and (
        ignore_outer_edges
        <= (new_col := home_location[1] + distance * direction.value[1])
        <= num_cols - 1 - ignore_outer_edges
    ):
        scenic_score += 1
        if grid[new_row, new_col] >= grid[home_location]:
            # This exit condition can only be evaluated after the scenic score was
            # increased.
            break
        distance += 1
    return scenic_score


def get_scenic_score(grid: np.ndarray, tree_index: tuple[int, int]) -> np.int32:
    """Get the scenic score for the tree at the given tree_index in the tree
    grid."""
    directional_scenic_score = np.array(
        [
            scan_along_direction(grid, tree_index, direction, ignore_outer_edges=True)
            for direction in [
                Direction.LEFT,
                Direction.UP,
                Direction.RIGHT,
                Direction.DOWN,
            ]
        ]
    )
    scenic_score = np.product(directional_scenic_score)
    return scenic_score


def check_scenic_scores(grid: np.ndarray) -> np.ndarray:
    """Calculate the scenic scores of all trees in the grid and add them inplace
    to the scenic_scores array"""
    scenic_scores = np.zeros_like(grid)
    with np.nditer(
        scenic_scores[1:-1, 1:-1], op_flags=["readwrite"], flags=["multi_index"]
    ) as it:
        for score_entry in it:
            score_entry[...] = get_scenic_score(grid, it.multi_index)
    return scenic_scores


def part1(grid: np.ndarray) -> np.int32:
    """Advent of code 2022 day 8 - Part 1"""
    visibility_grid = np.zeros_like(grid)
    check_visibility(grid, visibility_grid)
    answer = np.sum(visibility_grid)  # np.int32
    print(f"Solution day 8, part 1: {answer}")
    return answer


def part2(grid: np.ndarray) -> np.int32:
    """Advent of code 2022 day 8 - Part 2"""
    scenic_scores = check_scenic_scores(grid)
    answer = np.max(scenic_scores)

    print(f"Solution day 8, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input8.1'
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
            submit(aocd_result, part=part, day=8, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    submit_answer = False
    # submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    main("ab", should_submit=submit_answer, load_test_data=test_data)
