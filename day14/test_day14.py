# Unit testing
"""
@author: Tobias Van Damme
"""

import unittest
import json
from pathlib import Path

import numpy as np

import helper_functions
from . import day14

TEST_FOLDER = Path(__file__).parent

with open(TEST_FOLDER / "input14.1", "r") as f:
    # For loading example or test data
    TEST_DATA = f.read()


class TestDay14(unittest.TestCase):
    """Test class to test functions in day14.day14"""

    def setUp(self):
        """Setup the tests"""
        pass

    def tearDown(self):
        """Clean up"""
        pass

    def test_construct_grid(self):
        """Test day14.construct_grid"""
        height, width, left = day14.get_grid_dimensions(TEST_DATA)
        print(f'{height = }, {width = }, {left = }')
        line_segments, _ = day14.build_line_segments(TEST_DATA.splitlines())
        grid = day14.construct_grid(line_segments, height)
        # print(grid)
        day14.print_grid(grid)


if __name__ == "__main__":
    unittest.main(module="test_day14")
