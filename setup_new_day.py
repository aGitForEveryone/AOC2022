import argparse
from pathlib import Path
from datetime import datetime
import textwrap

DESCRIPTION = "Advent of code initialization script"
CURRENT_DIRECTORY = Path(__file__).parent


if __name__ == "__main__":
    arguments = argparse.ArgumentParser(description=DESCRIPTION)
    arguments.add_argument(
        "day",
        type=int,
        choices=range(0, 26),
        default=0,
        nargs="?",
        help="Select the target day for which to initialize the puzzle. If not "
        "supplied or 0 is given, then today's puzzle will be fetched.",
        metavar="PUZZLE_DAY",
    )
    args = arguments.parse_args()
    target_day = args.day
    if target_day == 0:
        # Fetch today's date
        target_day = datetime.now().day
        current_month = datetime.now().month
        # If the script is called outside of advent of codes running time, then
        # the default argument doesn't work
        if current_month != 12 or target_day > 25:
            raise ValueError(
                f"You are trying to initialize puzzle code for aoc 2022 outside "
                f"it's normal running time (December 1 to 25). Please specify "
                f"the day for which code should be initialized by passing a "
                f"number on the CLI, e.g.:\n"
                f">>> python setup_new_day.py <day>"
            )

    target_directory = CURRENT_DIRECTORY / f"day{target_day:0>2}"
    if target_directory.exists():
        raise OSError(
            f"Directory for target AOC day (year 2022) already exists "
            f"(requested day {target_day}).\n"
            f"PLease manually remove the target directory: {target_directory}"
        )

    target_directory.mkdir()

    template_code = textwrap.dedent(
        f"""\
    import re
    
    from aocd import get_data, submit
    import numpy as np
    
    import helper_functions
    from helper_functions import Coordinate
    
    
    def parse_data(load_test_data: bool = False):
        \"\"\"Parser function to parse today's data
        
        Args:
            load_test_data:     Set to true to load test data from the local 
                                directory
        \"\"\"
        if load_test_data:
            with open("input{target_day}.1", "r") as f:
                # For loading example or test data
                data = f.read()
        else:
            data = get_data(day={target_day}, year=2022)
        # lines = data.splitlines()
        # grid = np.array(helper_functions.digits_to_int(data.splitlines()))
        # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
        return data
    
    
    def part1(data):
        \"\"\"Advent of code 2022 day {target_day} - Part 1\"\"\"
        answer = 0
        
        print(f"Solution day {target_day}, part 1: {{answer}}")
        return answer
    
        
    def part2(data):
        \"\"\"Advent of code 2022 day {target_day} - Part 2\"\"\"
        answer = 0
        
        print(f"Solution day {target_day}, part 2: {{answer}}")
        return answer
        
    
    def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
        \"\"\"Main function for solving the selected part(s) of today's puzzle
        and automatically submitting the answer. 
        
        Args:
            parts:          "a", "b", or "ab". Execute the chosen parts
            should_submit:  Set to True if you want to submit your answer
            load_test_data: Set to True if you want to load test data instead of
                            the full input. By default, this will load the file 
                            called 'input{target_day}.1'
        \"\"\"
        data = parse_data(load_test_data=load_test_data)
        
        for part in parts:
            if part == "a":
                aocd_result = part1(data)
            elif part == "b":
                aocd_result = part2(data)
            else:
                raise ValueError(f"Wrong part chosen, expecting 'a' or 'b': got {{part}}")
    
            if should_submit:
                submit(aocd_result, part=part, day={target_day}, year=2022)
        
        
    if __name__ == "__main__":
        test_data = False
        # test_data = True
        submit_answer = False
        # submit_answer = True
        main("a", should_submit=submit_answer, load_test_data=test_data)
        # main("b", should_submit=submit_answer, load_test_data=test_data)
        # main("ab", should_submit=submit_answer, load_test_data=test_data)
    """
    )

    with open(target_directory / f"day{target_day}.py", "w+") as f:
        f.write(template_code)

    with open(target_directory / f"input{target_day}.1", "w+") as f:
        f.write('')

    template_code_tests = textwrap.dedent(
        f"""\
    # Unit testing
    \"\"\"
    @author: Tobias Van Damme
    \"\"\"
    
    import unittest
    import json
    from pathlib import Path
    
    import numpy as np
    
    import helper_functions
    from . import day{target_day}
    
    TEST_FOLDER = Path(__file__).parent
    
    with open(TEST_FOLDER / "input{target_day}.1", "r") as f:
        # For loading example or test data
        TEST_DATA = f.read()
    
    
    class TestDay{target_day}(unittest.TestCase):
        \"\"\"Test class to test functions in day{target_day:0>2}.day{target_day}\"\"\"
    
        def setUp(self):
            \"\"\"Setup the tests\"\"\"
            pass
    
        def tearDown(self):
            \"\"\"Clean up\"\"\"
            pass
    
        def test_part1(self):
            \"\"\"Test day{target_day}.part1\"\"\"
            result = day{target_day}.part1(TEST_DATA)
    
    
    if __name__ == "__main__":
        unittest.main(module="test_day{target_day}")

    """
    )

    with open(target_directory / f"test_day{target_day}.py", "w+") as f:
        f.write(template_code_tests)

