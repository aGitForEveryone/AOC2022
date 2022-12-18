import re
from typing import Optional

from aocd import get_data, submit
import numpy as np

import helper_functions
from helper_functions import Coordinate, LineSegment


def get_coordinates(data: list[str]) -> tuple[tuple[Coordinate, Coordinate, int]]:
    """From the input parse the sensor and closest beacon coordinates and the
    manhattan distance between the two"""
    sensor_beacon_sets = []
    for line in data:
        coordinates = [
            Coordinate(coordinate)
            for coordinate in helper_functions.digits_to_int(
                re.findall(f"x=(-?\d+), y=(-?\d+)", line), individual_character=False
            )
        ]
        distance_beacon_sensor = coordinates[0].manhattan_distance(coordinates[1])
        sensor_beacon_sets.append(tuple((coordinates + [distance_beacon_sensor])))
    return tuple(sensor_beacon_sets)


def parse_data(load_test_data: bool = False):
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local
                            directory
    """
    if load_test_data:
        with open("input15.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=15, year=2022)
    lines = data.splitlines()
    # grid = np.array(helper_functions.digits_to_int(data.splitlines()))
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return get_coordinates(lines)


def coordinates_in_reach(
    sensor_location: Coordinate, sensing_distance: int, target_y: int
) -> Optional[LineSegment]:
    """Get the set of coordinates on the target_y row that is within the sensing
    distance of the sensor"""
    y_distance = abs(target_y - sensor_location[1])
    if y_distance > sensing_distance:
        # Then the sensor cannot reach the target row
        return None
    remaining_distance = sensing_distance - y_distance
    lowest_x = sensor_location[0] - remaining_distance
    highest_x = sensor_location[0] + remaining_distance
    return LineSegment(Coordinate(lowest_x, target_y), Coordinate(highest_x, target_y))


def merge_all_lines(lines: list[LineSegment]) -> list[LineSegment]:
    """Merge all line segments in the list that can be merged"""
    merged_lines = []
    # print(f"{lines = }")
    while len(lines):
        line = lines.pop()
        # print(f"{line = }")
        # print(f"{lines = }")
        idx = 0
        merged_line_idx = set()
        while idx < len(lines):
            if idx in merged_line_idx:
                # if we already processed this line, continue
                idx += 1
                continue
            if (merged_line := line.merge(lines[idx])) != line:
                # We were able to merge the lines. Reset index to zero as we
                # need to check all previously checked lines again. Maybe now,
                # we are able to merge them.
                # print(
                #     f"We can merge at {idx = }: other line {lines[idx]}, current line {line}, merged line {merged_line}"
                # )
                line = merged_line
                merged_line_idx.add(idx)
                idx = 0
            else:
                idx += 1
        merged_lines += [line]
        # Collect all remaining line segments and see if we can create a second
        # merged line segment.
        lines = [lines[idx] for idx in range(len(lines)) if idx not in merged_line_idx]

    return merged_lines


def part1(sensor_beacons: tuple[tuple[Coordinate, Coordinate, int]]) -> int:
    """Advent of code 2022 day 15 - Part 1"""
    target_y = 2000_000
    target_y = 10
    beacons_on_target_y = 0
    impossible_locations = []
    for sensor_location, beacon_location, distance in sensor_beacons:
        # print(f'{sensor_location = }, {beacon_location = }, {distance = }')
        if beacon_location[1] == target_y:
            # Remember that this beacon is located on the target row, so we can
            # subtract that from the total available spaces
            beacons_on_target_y += 1
        covered_location = coordinates_in_reach(sensor_location, distance, target_y)
        if covered_location:
            # print(f'{covered_location = }')
            impossible_locations += [covered_location]

    impossible_locations = merge_all_lines(impossible_locations)
    # print(f"{beacons_on_target_y = }")
    # print(f"{impossible_locations = }")

    # We should subtract the number of beacons that exist on the target_y
    answer = -beacons_on_target_y
    for line in impossible_locations:
        # print(f"{len(line) = }")
        answer += len(line)

    print(f"Solution day 15, part 1: {answer}")
    return answer


def part2(data):
    """Advent of code 2022 day 15 - Part 2"""
    answer = 0

    print(f"Solution day 15, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input15.1'
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
            submit(aocd_result, part=part, day=15, year=2022)


if __name__ == "__main__":
    # test_data = False
    test_data = True
    submit_answer = False
    # submit_answer = True
    main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    # main("ab", should_submit=submit_answer, load_test_data=test_data)
