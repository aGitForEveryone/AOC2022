# Unit testing
"""
@author: Tobias Van Damme
"""

import unittest
import json
from pathlib import Path

import numpy as np

import helper_functions
from . import day11

TEST_FOLDER = Path(__file__).parent

with open(TEST_FOLDER / "input11.1", "r") as f:
    # For loading example or test data
    data = f.read()
    monkeys = day11.parse_monkeys(data.split("\n\n"))


class TestDay11(unittest.TestCase):
    """Test class to test functions in day11.day11"""

    def setUp(self):
        """Setup the tests"""
        pass

    def tearDown(self):
        """Clean up"""
        pass

    def test_worry_level_updater(self):
        """Test day11.relevant_clock_cycles"""
        print(monkeys)
        print(day11.print_item_lists(monkeys))
        # worry_level = 79
        # new_worry_level = monkeys[0].update_worry_level(worry_level)
        # operation = 'old * 19'
        # test = lambda old: eval(operation)
        # assert 1501 == test(worry_level), f'test: {new_worry_level = }, expected 1501'
        print(f"{monkeys[0].update_worry_level(2) = }")
        print(f"{monkeys[1].update_worry_level(2) = }")
        print(f"{monkeys[2].update_worry_level(2) = }")
        print(f"{monkeys[3].update_worry_level(2) = }")
        print(f"{monkeys[0].test_worry_level(23) = }")
        print(f"{monkeys[1].test_worry_level(19) = }")
        print(f"{monkeys[2].test_worry_level(13) = }")
        print(f"{monkeys[3].test_worry_level(17) = }")
        # assert new_worry_level == 1501, f'{new_worry_level = }, expected 1501'


if __name__ == "__main__":
    unittest.main(module="test_day11")
