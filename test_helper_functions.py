# Unit testing
"""
@author: Tobias Van Damme
"""
import itertools
import math
import unittest
import json
from pathlib import Path
from typing import Callable

import numpy as np

import helper_functions
from helper_functions import Coordinate


TEST_FOLDER = Path(__file__).parent


class TestHelperFunctions(unittest.TestCase):
    """Test class to test functions in helper_functions"""

    def setUp(self):
        """Setup the tests"""
        pass

    def tearDown(self):
        """Clean up"""
        pass

    def test_digits_to_int(self):
        """Test helper_functions.digits_to_int"""
        string_num = "12345"
        test_grid = ["30373", "25512", "65332", "33549", "35390"]
        individual_digits = [False, True]

        # Test if single string is processed successfully
        expected_result = [12345, [1, 2, 3, 4, 5]]
        for individual_digit, result in zip(individual_digits, expected_result):
            assert (
                helper_functions.digits_to_int(string_num, individual_digit) == result
            )

        assert helper_functions.digits_to_int(string_num, True, return_type=tuple) == (
            1,
            2,
            3,
            4,
            5,
        )
        assert helper_functions.digits_to_int(string_num, True, return_type=tuple) != [
            1,
            2,
            3,
            4,
            5,
        ]

        # Test if grid is processed successfully
        expected_result = [
            [30373, 25512, 65332, 33549, 35390],
            [
                [3, 0, 3, 7, 3],
                [2, 5, 5, 1, 2],
                [6, 5, 3, 3, 2],
                [3, 3, 5, 4, 9],
                [3, 5, 3, 9, 0],
            ],
        ]
        for individual_digit, result in zip(individual_digits, expected_result):
            assert (
                actual_result := helper_functions.digits_to_int(
                    test_grid, individual_digit
                )
            ) == result, (
                f"Grid strings not processed correctly where {individual_digit = }.\n"
                f"Expected result: {result}\n"
                f"Actual result: {actual_result}"
            )
        expected_result_tuple = [
            (30373, 25512, 65332, 33549, 35390),
            (
                (3, 0, 3, 7, 3),
                (2, 5, 5, 1, 2),
                (6, 5, 3, 3, 2),
                (3, 3, 5, 4, 9),
                (3, 5, 3, 9, 0),
            ),
        ]
        for individual_digit, result in zip(individual_digits, expected_result_tuple):
            assert (
                actual_result := helper_functions.digits_to_int(
                    test_grid, individual_digit, return_type=tuple
                )
            ) == result, (
                f"Grid strings not processed correctly where {individual_digit = }.\n"
                f"Expected result: {result}\n"
                f"Actual result: {actual_result}"
            )

    def test_pad_numpy_array(self):
        """Test helper_functions.pad_numpy_array"""
        test_grid = np.array([[1, 2], [3, 4]])

        padded_grid = np.array(
            [[-1, -1, -1, -1], [-1, 1, 2, -1], [-1, 3, 4, -1], [-1, -1, -1, -1]]
        )
        # Default settings
        np.testing.assert_array_equal(
            helper_functions.pad_numpy_array(test_grid, -1), padded_grid
        )
        # pad_width as int
        np.testing.assert_array_equal(
            helper_functions.pad_numpy_array(test_grid, -1, pad_width=1), padded_grid
        )

        # Padded with 1 line before and 2 lines after for each axis
        unequal_padded_grid = np.array(
            [
                [-1, -1, -1, -1, -1],
                [-1, 1, 2, -1, -1],
                [-1, 3, 4, -1, -1],
                [-1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1],
            ]
        )
        np.testing.assert_array_equal(
            helper_functions.pad_numpy_array(test_grid, -1, pad_width=(1, 2)),
            unequal_padded_grid,
        )

        # Padded a different number of lines for each axis
        specific_padded_grid = np.array(
            [
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, 1, 2, -1, -1, -1, -1],
                [-1, -1, -1, 3, 4, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            ]
        )
        np.testing.assert_array_equal(
            helper_functions.pad_numpy_array(test_grid, -1, pad_width=((1, 2), (3, 4))),
            specific_padded_grid,
        )

    def test_coordinate(self):
        """Test coordinate class"""
        coordinate1 = Coordinate(1, 2)
        coordinate2 = Coordinate(3, 4)
        coordinate3 = Coordinate(-2, 49)
        assert coordinate1 + coordinate2 == (4, 6)
        assert coordinate1 + coordinate3 == (-1, 51)

        assert coordinate1.distance(coordinate2) == math.sqrt(8)

        assert not coordinate1.is_touching(coordinate2)
        distances = [(0, 1), (0, 0), (1, 1), (-1, 1), (1, 0), (-1, 0)]
        not_diagonal = [True, True, False, False, True, True]
        for distance, touching_diagonally in zip(distances, not_diagonal):
            assert coordinate1.is_touching(coordinate1 + distance)
            assert (
                coordinate1.is_touching(coordinate1 + distance, diagonal=False)
                == touching_diagonally
            ), (
                f"Testing touching cardinal directions only, "
                f"expected: {touching_diagonally}, got "
                f"{coordinate1.is_touching(coordinate1 + distance, diagonal=False)} "
                f"for coordinate at {coordinate1} and distance {distance}"
            )

        assert not coordinate1.is_touching(coordinate1, overlap=False)
        assert coordinate1.is_touching(coordinate1, overlap=True)

        assert coordinate2 > coordinate1
        assert coordinate1 < coordinate2
        assert coordinate2 >= coordinate1 + (0, 2)
        assert coordinate1 <= coordinate2 - (2, 0)

        # Test creation of origin
        assert Coordinate.create_origin() == Coordinate(0, 0)
        assert Coordinate.create_origin(3) == Coordinate(0, 0, 0)

        # Test manhattan distance
        assert coordinate1.manhattan_distance(coordinate2) == 4

    def test_get_sign(self):
        """Test helper_functions.get_sign"""
        assert helper_functions.get_sign(-5) == -1
        assert helper_functions.get_sign(0) == 0
        assert helper_functions.get_sign(0, sign_zero=1) == 1
        assert helper_functions.get_sign(2.5465) == 1

    def test_line_segment(self):
        """Test helper_functions.LineSegment"""
        line1 = helper_functions.LineSegment(Coordinate(2, 10), Coordinate(18, 10))
        line2 = helper_functions.LineSegment(Coordinate(12, 10), Coordinate(12, 10))
        print(line1.merge(line2))

    def test_manual(self):
        """Some manual testing"""
        print(f"{type(helper_functions.Direction.LEFT.value)}")

    def test_full_space(self):
        """Test helper_functions.full_space"""
        # 3D space
        space_limits = (Coordinate(0, 0, 0), Coordinate(2, 2, 2))
        expected_coordinates = [
            (0, 0, 0),
            (0, 0, 1),
            (0, 0, 2),
            (0, 1, 0),
            (0, 1, 1),
            (0, 1, 2),
            (0, 2, 0),
            (0, 2, 1),
            (0, 2, 2),
            (1, 0, 0),
            (1, 0, 1),
            (1, 0, 2),
            (1, 1, 0),
            (1, 1, 1),
            (1, 1, 2),
            (1, 2, 0),
            (1, 2, 1),
            (1, 2, 2),
            (2, 0, 0),
            (2, 0, 1),
            (2, 0, 2),
            (2, 1, 0),
            (2, 1, 1),
            (2, 1, 2),
            (2, 2, 0),
            (2, 2, 1),
            (2, 2, 2),
        ]
        filled_coordinates = helper_functions.full_space(*space_limits)
        assert len(filled_coordinates) == len(expected_coordinates), (
            f"Number of filled coordinates: {len(filled_coordinates)}, "
            f"number of expected coordinates: {len(expected_coordinates)}"
        )
        for coordinate in expected_coordinates:
            assert coordinate in filled_coordinates

        # 2d space
        space_limits = (Coordinate(0, 0), Coordinate(2, 3))
        expected_coordinates = [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
        ]
        filled_coordinates = helper_functions.full_space(*space_limits)
        assert len(filled_coordinates) == len(expected_coordinates), (
            f"Number of filled coordinates: {len(filled_coordinates)}, "
            f"number of expected coordinates: {len(expected_coordinates)}"
        )
        for coordinate in expected_coordinates:
            assert coordinate in filled_coordinates

    def test_flood_fill(self):
        """Test helper_functions.flood_fill"""

        def check_condition(
            space_limits: tuple[Coordinate, Coordinate],
            is_valid_coordinate: Callable,
            expected_coordinates: list[Coordinate],
        ) -> None:
            """Do test in the given space with the given valid coordinate checker"""
            filled_coordinate = helper_functions.flood_fill(
                space_limits[0], is_valid_coordinate
            )
            assert len(filled_coordinate) == len(expected_coordinates), (
                f"Number of filled coordinates: {len(filled_coordinate)}, "
                f"number of expected coordinates: {len(expected_coordinates)}"
            )
            for coordinate in expected_coordinates:
                assert coordinate in filled_coordinate

        # 3D full space
        def accept_full_space(coordinate: Coordinate) -> bool:
            return space_limits[0] <= coordinate <= space_limits[1]

        space_limits = Coordinate(0, 0, 0), Coordinate(2, 2, 2)
        check_condition(
            space_limits=space_limits,
            is_valid_coordinate=accept_full_space,
            expected_coordinates=helper_functions.full_space(*space_limits),
        )

        # 2D space with wall in middle
        def wall_in_middle(coordinate: Coordinate) -> bool:
            """Wall in the second row"""
            return (space_limits[0] <= coordinate <= space_limits[1]) and (
                coordinate[0] < 2
            )

        space_limits = (Coordinate(0, 0), Coordinate(3, 4))
        expected_coordinates = [
            Coordinate(coordinate)
            for coordinate in [
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (0, 4),
                (1, 0),
                (1, 1),
                (1, 2),
                (1, 3),
                (1, 4),
            ]
        ]
        check_condition(
            space_limits=space_limits,
            is_valid_coordinate=wall_in_middle,
            expected_coordinates=expected_coordinates,
        )


if __name__ == "__main__":
    unittest.main(module="test_helper_functions")
