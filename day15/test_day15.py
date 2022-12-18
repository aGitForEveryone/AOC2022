# Unit testing
"""
@author: Tobias Van Damme
"""

import unittest
import json
from pathlib import Path

import numpy as np

import helper_functions
from . import day15

TEST_FOLDER = Path(__file__).parent

with open(TEST_FOLDER / "input15.1", "r") as f:
    # For loading example or test data
    TEST_DATA = f.read()


class TestDay15(unittest.TestCase):
    """Test class to test functions in day15.day15"""

    def setUp(self):
        """Setup the tests"""
        pass

    def tearDown(self):
        """Clean up"""
        pass

    def test_part1(self):
        """Test day15.part1"""
        result = day15.part1(TEST_DATA)


if __name__ == "__main__":
    unittest.main(module="test_day15")

