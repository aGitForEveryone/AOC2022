# Unit testing
"""
@author: Tobias Van Damme
"""
import unittest
import json
from pathlib import Path

import numpy as np

import helper_functions


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


if __name__ == "__main__":
    unittest.main(module="test_helper_functions")
