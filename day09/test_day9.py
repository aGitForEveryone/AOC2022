# Unit testing
"""
@author: Tobias Van Damme
"""

import unittest
import json
from pathlib import Path

import numpy as np

import helper_functions
from helper_functions import Coordinate
from . import day9


TEST_FOLDER = Path(__file__).parent


class TestDay9(unittest.TestCase):
    """Test class to test functions in day09.day9"""

    def setUp(self):
        """Setup the tests"""
        pass

    def tearDown(self):
        """Clean up"""
        pass

    def test_move_tail(self):
        """Test day9.move_tail"""
        location_tail = Coordinate(3, 3)
        location_head = [
            Coordinate(row, col) for row in range(1, 6) for col in range(1, 6)
        ]
        expected_tail_location = [
            Coordinate(2, 2),
            Coordinate(2, 2),
            Coordinate(2, 3),
            Coordinate(2, 4),
            Coordinate(2, 4),
            Coordinate(2, 2),
            Coordinate(3, 3),
            Coordinate(3, 3),
            Coordinate(3, 3),
            Coordinate(2, 4),
            Coordinate(3, 2),
            Coordinate(3, 3),
            Coordinate(3, 3),
            Coordinate(3, 3),
            Coordinate(3, 4),
            Coordinate(4, 2),
            Coordinate(3, 3),
            Coordinate(3, 3),
            Coordinate(3, 3),
            Coordinate(4, 4),
            Coordinate(4, 2),
            Coordinate(4, 2),
            Coordinate(4, 3),
            Coordinate(4, 4),
            Coordinate(4, 4),
        ]
        assert len(expected_tail_location) == len(location_head)

        for head, expected_location in zip(location_head, expected_tail_location):
            new_location = day9.move_tail(location_tail, head)
            assert new_location == expected_location, (
                f"Location head: {head}, location tail: {location_tail}\n"
                f"Expected new location: {expected_location}\n"
                f"Actual new location: {new_location}"
            )


if __name__ == "__main__":
    unittest.main(module="test_day9")
