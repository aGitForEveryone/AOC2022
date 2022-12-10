# Unit testing
"""
@author: Tobias Van Damme
"""

import unittest
import json
from pathlib import Path

import numpy as np

import helper_functions
from . import day10


TEST_FOLDER = Path(__file__).parent


class TestDay10(unittest.TestCase):
    """Test class to test functions in day10.day10"""

    def setUp(self):
        """Setup the tests"""
        pass

    def tearDown(self):
        """Clean up"""
        pass

    def test_relevant_clock_cycles(self):
        """Test day10.relevant_clock_cycles"""
        clock_cycles = [10, 20, 30, 40, 50, 60, 220, 180]
        should_evaluate = [False, True, False, False, False, True, True, True]
        for clock_cycle, evaluate in zip(clock_cycles, should_evaluate):
            assert day10.relevant_clock_cycles(clock_cycle) == evaluate, \
                f'Current clock cycle: {clock_cycle}\n' \
                f'expected to evaluate: {evaluate}\n' \
                f'will evaluate: {day10.relevant_clock_cycles(clock_cycle)}'



if __name__ == "__main__":
    unittest.main(module="test_day10")
