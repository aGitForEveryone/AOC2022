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
        help="Select the target day for which to initialize the puzzle. If not "
        "supplied or 0 is given, then today's puzzle will be fetched.",
        metavar="PUZZLE_DAY",
    )
    args = arguments.parse_args()
    target_day = args.day
    if target_day == 0:
        # Fetch today's date
        target_day = datetime.now().day

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
    
    data = get_data(day={target_day}, year=2022)
    lines = data.splitlines()
    numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    
    
    def part1():
        \"\"\"Advent of code 2022 day {target_day} - Part 1\"\"\"
        answer = 0
        
        print(f"Solution day {target_day}, part 1: {{answer}}")
        return answer
    
        
    def part2():
        \"\"\"Advent of code 2022 day {target_day} - Part 2\"\"\"
        answer = 0
        
        print(f"Solution day {target_day}, part 2: {{answer}}")
        return answer
        
    
    if __name__ == "__main__":
        part = "a"
        # part = "b"
        submit_answer = False

        aocd_result = part1() if part == "a" else part2()
        if submit_answer:
            submit(aocd_result, part=part, day={target_day}, year=2022)
    """
    )

    with open(target_directory / f"day{target_day}.py", "w+") as f:
        f.write(template_code)
