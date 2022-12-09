# Unit testing
"""
@author: Tobias Van Damme
"""

import unittest
import json
from pathlib import Path

import numpy as np

import helper_functions
from . import day8


TEST_FOLDER = Path(__file__).parent

TEST_GRID = helper_functions.pad_numpy_array(
    np.array(
        helper_functions.digits_to_int(["30373", "25512", "65332", "33549", "35390"])
    ),
    -1,
)


class TestDay8(unittest.TestCase):
    """Test class to test functions in day08.day8"""

    def setUp(self):
        """Setup the tests"""
        pass

    def tearDown(self):
        """Clean up"""
        pass

    def test_scan_along_direction(self):
        """Test day8.scan_along_direction"""
        test_data = {
            (4, 3): {
                day8.Direction.UP: 2,
                day8.Direction.LEFT: 2,
                day8.Direction.DOWN: 1,
                day8.Direction.RIGHT: 2,
            },
            (2, 3): {
                day8.Direction.UP: 1,
                day8.Direction.LEFT: 1,
                day8.Direction.DOWN: 2,
                day8.Direction.RIGHT: 2,
            },
        }
        for home_location, expected_result in test_data.items():
            for direction, line_of_sight in expected_result.items():
                assert (
                    day8.scan_along_direction(
                        TEST_GRID, home_location, direction, ignore_outer_edges=True
                    )
                    == line_of_sight
                )


if __name__ == "__main__":
    unittest.main(module="test_day8")
