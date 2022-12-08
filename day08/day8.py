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
        with open("input8.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=8, year=2022)
    lines = data.splitlines()
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return lines


def create_number_grid(data: list[str], extra_row_symbol: int = None) -> np.ndarray:
    """Create a numpy array from a grid of string numbers. If extra_row_symbol
    is given, the grid will be enlarged by 1 row/column on each side, filled
    with the value given."""
    number_grid = [[int(number) for number in line] for line in data]
    grid = np.asarray(number_grid)

    if extra_row_symbol is not None:
        # Pad the grid with an extra row/column on each side
        grid = np.pad(grid, ((1, 1), (1, 1)), 'constant',
                      constant_values=extra_row_symbol)

    return grid


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


def get_scenic_score(grid: np.ndarray, tree_index: tuple[int, int]) -> np.int32:
    """Get the scenic score for the tree at the given tree_index in the tree
    grid."""
    tree_row, tree_col = tree_index
    tree_height = grid[tree_row, tree_col]
    num_rows, num_cols = grid.shape
    # [left, top, right, bottom]
    directional_scenic_score = np.array([0, 0, 0, 0])
    view_blocked = [False, False, False, False]
    left_idx = 0
    top_idx = 1
    right_idx = 2
    bottom_idx = 3
    distance = 1
    while not all(view_blocked):
        # left
        if not view_blocked[left_idx] and tree_col - distance > 0:
            directional_scenic_score[left_idx] += 1
            if grid[tree_row, tree_col - distance] >= tree_height:
                view_blocked[left_idx] = True
        else:
            view_blocked[left_idx] = True
        # top
        if not view_blocked[top_idx] and tree_row - distance > 0:
            directional_scenic_score[top_idx] += 1
            if grid[tree_row - distance, tree_col] >= tree_height:
                view_blocked[top_idx] = True
        else:
            view_blocked[top_idx] = True
        # right
        if not view_blocked[right_idx] and tree_col + distance < num_cols - 1:
            directional_scenic_score[right_idx] += 1
            if grid[tree_row, tree_col + distance] >= tree_height:
                view_blocked[right_idx] = True
        else:
            view_blocked[right_idx] = True
        # bottom
        if not view_blocked[bottom_idx] and tree_row + distance < num_rows - 1:
            directional_scenic_score[bottom_idx] += 1
            if grid[tree_row + distance, tree_col] >= tree_height:
                view_blocked[bottom_idx] = True
        else:
            view_blocked[bottom_idx] = True
        distance += 1
    scenic_score = np.product(directional_scenic_score)
    # print(f'{tree_index = }, {directional_scenic_score = }, {scenic_score = }')
    return scenic_score


def check_scenic_scores(grid: np.ndarray, scenic_scores: np.ndarray) -> None:
    """Calculate the scenic scores of all trees in the grid and add them inplace
    to the scenic_scores array"""
    num_rows, num_cols = grid.shape
    for row in range(1, num_rows):
        for col in range(1, num_cols):
            scenic_scores[row, col] = get_scenic_score(grid, (row, col))


def part1(grid: np.ndarray) -> np.int32:
    """Advent of code 2022 day 8 - Part 1"""
    visibility_grid = np.zeros_like(grid)
    check_visibility(grid, visibility_grid)
    # print(visibility_grid)
    answer = np.sum(visibility_grid)  # np.int32
    print(f"Solution day 8, part 1: {answer}")
    return answer


def part2(grid: np.ndarray) -> np.int32:
    """Advent of code 2022 day 8 - Part 2"""
    scenic_scores = np.zeros_like(grid)
    # print(grid)
    check_scenic_scores(grid, scenic_scores)
    # print(scenic_scores)
    answer = np.max(scenic_scores)

    # print(f'{type(answer) = }')
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
    data = create_number_grid(data, -1)

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
    # submit_answer = False
    submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    main("b", should_submit=submit_answer, load_test_data=test_data)
    # main("ab", should_submit=submit_answer, load_test_data=test_data)
