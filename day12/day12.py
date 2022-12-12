from typing import Callable

from aocd import get_data, submit

from helper_functions import Coordinate, Direction


START_SYMBOL: str = "S"
END_SYMBOL: str = "E"


def parse_data(load_test_data: bool = False) -> list[str]:
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local
                            directory
    """
    if load_test_data:
        with open("input12.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=12, year=2022)
    lines = data.splitlines()
    # grid = np.array(helper_functions.digits_to_int(data.splitlines()))
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return lines


def find_start_and_end_coordinate(grid: list[str]) -> dict[str, Coordinate]:
    """Look for the S and E indicating the start and end position accordingly
    return a dict containing the coordinates to each position"""
    start_end = {"start": None, "end": None}
    for line_idx, line in enumerate(grid):
        if (start_idx := line.find(START_SYMBOL)) >= 0:
            start_end["start"] = Coordinate(line_idx, start_idx)
        if (end_idx := line.find(END_SYMBOL)) >= 0:
            start_end["end"] = Coordinate(line_idx, end_idx)
    return start_end


def is_coordinate_in_grid(location: Coordinate, grid: list[str]) -> bool:
    """Check if coordinate is in grid boundaries"""
    return Coordinate(0, 0) <= location < Coordinate(len(grid), len(grid[0]))


def is_go_up_valid(current_location: str, next_location: str) -> bool:
    """Part 1 move rules. Next location is valid if it is at most one character
    later in the alphabet. For example, if current location is l, then [a-m] are
    valid next locations"""

    def replace_special_symbols(symbol: str) -> str:
        if symbol == START_SYMBOL:
            return "a"
        elif symbol == END_SYMBOL:
            return "z"

        # Else return the symbol itself
        return symbol

    return (
        ord(replace_special_symbols(next_location))
        - ord(replace_special_symbols(current_location))
    ) <= 1


def get_possible_next_locations(
    cur_location: Coordinate,
    grid: list[str],
    visited: dict[Coordinate, int],
    is_move_valid: Callable,
) -> list[Coordinate]:
    """List all the possible next locations you can visit from the current
    location"""
    next_locations = []
    for direction in Direction:
        if (
            (next_location := cur_location + direction.value) not in visited
            and is_coordinate_in_grid(next_location, grid)
            and is_move_valid(
                grid[cur_location[0]][cur_location[1]],
                grid[next_location[0]][next_location[1]],
            )
        ):
            next_locations += [next_location]

    return next_locations


def move(
    current_frontier: list[Coordinate],
    grid: list[str],
    visited: dict[Coordinate, int],
    is_move_valid: Callable,
) -> (list[Coordinate], dict[Coordinate, int]):
    """From cur_location retrieve all possible next location that are still
    unvisited"""

    next_frontier = []
    for cur_location in current_frontier:
        for next_location in get_possible_next_locations(
            cur_location, grid, visited, is_move_valid
        ):
            visited[next_location] = visited[cur_location] + 1
            next_frontier += [next_location]

    return next_frontier, visited


def shortest_path(
    start_location: Coordinate,
    end_location: Coordinate,
    grid: list[str],
    is_move_valid: Callable,
) -> int:
    """Search for the shortest path from start to end in the grid. Valid moves
    are defined by the callable is_move_valid (which takes two Coordinates as
    input, the current location and the next location as its first and second).

    Returns the number of steps needed to reach the end location
    """
    frontier = [start_location]
    visited = {start_location: 0}
    while end_location not in visited:
        frontier, visited = move(frontier, grid, visited, is_move_valid)
        if not frontier:
            # Then our search fails, and we have no more valid next locations
            # left
            return -1
    return visited[end_location]


def part1(grid: list[str]) -> int:
    """Advent of code 2022 day 12 - Part 1"""
    start_end = find_start_and_end_coordinate(grid)
    start = start_end["start"]
    end = start_end["end"]
    answer = shortest_path(start, end, grid, is_go_up_valid)

    print(f"Solution day 12, part 1: {answer}")
    return answer


def is_go_down_valid(current_location: str, next_location: str) -> bool:
    """Part 2 move rules. Next location is valid if it is at most one character
    lower in the alphabet. For example, if current location is l, then [k-z] are
    valid next locations"""

    def replace_special_symbols(symbol: str) -> str:
        if symbol == START_SYMBOL:
            return "a"
        elif symbol == END_SYMBOL:
            return "z"

        # Else return the symbol itself
        return symbol

    return (
        ord(replace_special_symbols(current_location))
        - ord(replace_special_symbols(next_location))
    ) <= 1


def get_characters_in_frontier(frontier: list[Coordinate], grid: list[str]) -> str:
    """Get the characters for each location in the frontier"""
    return "".join([grid[row][col] for row, col in frontier])


def shortest_path_to_a(
    start_location: Coordinate,
    grid: list[str],
    is_move_valid: Callable,
) -> int:
    """Search for the shortest path from the start in the grid to the lowest
    point in the valid. Valid moves are defined by the callable is_move_valid
    (which takes two Coordinates as input, the current location and the next
    location as its first and second).

    Returns the number of steps needed to reach the end location
    """
    frontier = [start_location]
    visited = {start_location: 0}
    frontier_characters = get_characters_in_frontier(frontier, grid)
    while not ("a" in frontier_characters or START_SYMBOL in frontier_characters):
        frontier, visited = move(frontier, grid, visited, is_move_valid)
        if not frontier:
            # Then our search fails, and we have no more valid next locations
            # left
            return -1
        frontier_characters = get_characters_in_frontier(frontier, grid)

    return visited[frontier[frontier_characters.find("a")]]


def part2(grid: list[str]) -> int:
    """Advent of code 2022 day 12 - Part 2"""
    start_end = find_start_and_end_coordinate(grid)
    start = start_end["end"]
    answer = shortest_path_to_a(start, grid, is_go_down_valid)

    print(f"Solution day 12, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input12.1'
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
            submit(aocd_result, part=part, day=12, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    submit_answer = False
    # submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    main("ab", should_submit=submit_answer, load_test_data=test_data)
