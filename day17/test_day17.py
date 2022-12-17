# Unit testing
"""
@author: Tobias Van Damme
"""

import unittest
import json
from pathlib import Path

import numpy as np

import helper_functions
from . import day17

TEST_FOLDER = Path(__file__).parent


class TestDay17(unittest.TestCase):
    """Test class to test functions in day17.day17"""

    def setUp(self):
        """Setup the tests"""
        pass

    def tearDown(self):
        """Clean up"""
        pass

    def test_jet_direction_data(self):
        """Test day17.jet_direction_data"""
        jet_streams = ">>><<><>>"
        for direction, next_direction in zip(
            jet_streams, day17.jet_direction_data(jet_streams)
        ):
            print(f"{next_direction = }")
            assert (
                direction == next_direction
            ), f"Expected {direction}, got {next_direction}"

        jet_iterator = day17.jet_direction_data(jet_streams)
        idx = 0
        while True:
            next_jet = jet_iterator


    def test_next_rock(self):
        """Test next_rock"""
        SYMBOL_ROCK = "#"
        SYMBOL_AIR = "."
        rocks = [
            [SYMBOL_ROCK * 4],
            [
                SYMBOL_AIR + SYMBOL_ROCK + SYMBOL_AIR,
                SYMBOL_ROCK * 3,
                SYMBOL_AIR + SYMBOL_ROCK + SYMBOL_AIR,
            ],
            [
                SYMBOL_AIR + SYMBOL_AIR + SYMBOL_ROCK,
                SYMBOL_AIR + SYMBOL_AIR + SYMBOL_ROCK,
                SYMBOL_ROCK * 3,
            ],
        [SYMBOL_ROCK, SYMBOL_ROCK, SYMBOL_ROCK, SYMBOL_ROCK],
        [SYMBOL_ROCK * 2, SYMBOL_ROCK * 2],
            [SYMBOL_ROCK * 4],
        ]
        for rock, next_rock in zip(rocks, day17.next_rock()):
            print(f"{rock = }")
            assert rock == next_rock, f"Expected {rock}, got {next_rock}"


if __name__ == "__main__":
    unittest.main(module="test_day17")
