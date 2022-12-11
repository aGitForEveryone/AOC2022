import os
from typing import Callable, Union

from aocd import get_data, submit
import numpy as np

import helper_functions
from helper_functions import Processor


def parse_data(load_test_data: bool = False):
    """Parser function to parse today's data

    Args:
        load_test_data:     Set to true to load test data from the local
                            directory
    """
    if load_test_data:
        with open("input10.1", "r") as f:
            # For loading example or test data
            data = f.read()
    else:
        data = get_data(day=10, year=2022)
    lines = data.splitlines()
    # grid = np.array(helper_functions.digits_to_int(data.splitlines()))
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return lines


class CathodeRayScreenProcessor(Processor):
    # Possible operations with their duration in clock cycles
    operations = {
        'noop': 1,
        'addx': 2
    }
    sprite = '###'
    pixel_on = helper_functions.Characters.WHITE_BLOCK.value
    pixel_off = ' '
    # screen size is: 40 pixels per row, 6 rows
    screen_rows = 6
    screen_pixels_per_row = 40
    screen = [pixel_off] * screen_pixels_per_row * screen_rows

    def __init__(self, memory: dict[str, int], clock: int,
                 evaluate_clock_cycle: Callable, evaluate_state: str = 'draw',
                 print_cycle: Callable = None
                 ) -> None:
        """Set the initial state of the processor

        Args:
            memory:                 each key-value pair is a memory cell with
                                    the value the cell contains
            clock:                  The initial state of the internal clock
            evaluate_clock_cycle:   Callable that takes the clock as an argument
                                    and return True if the internal processor
                                    state needs to be evaluated at that clock
                                    cycle.
            evaluate_state:         Callable takes the clock cycle and the
                                    memory as its input. Is called when the
                                    internal state is evaluated.
            """
        super().__init__(memory)
        self.clock = clock
        self.evaluate_clock_cycle = evaluate_clock_cycle

        match evaluate_state:
            case 'draw':
                self.evaluate_state = self.draw_pixel
            case 'signal_strength':
                self.evaluate_state = self.signal_strength

        if not print_cycle:
            self.print_cycle = lambda _: False
        else:
            self.print_cycle = print_cycle

        self.total_signal_strength = 0

    def update(self, instruction: str) -> None:
        """Perform the instruction and update the internal processor state"""
        match instruction.split():
            case ['noop']:
                for _ in range(self.operations['noop']):
                    self.update_clock()
            case ['addx', value]:
                for _ in range(self.operations['addx']):
                    self.update_clock()
                self.memory['x'] += int(value)
            case _:
                raise ValueError(f'Unknown instruction: {instruction}')

    def update_clock(self) -> None:
        """Updates the clock and checks whether the internal state needs to be
        evaluated"""
        self._evaluate_state()
        self._print_state()
        self.clock += 1

    def signal_strength(self) -> None:
        """Calculate the signal strength from the current memory state and the
        state of the clock"""
        signal_strength = self.clock * self.memory['x']
        self.total_signal_strength += signal_strength

    def draw_pixel(self) -> None:
        """Select the pixel to be drawn"""
        start_sprite = self.memory['x'] - len(self.sprite) // 2
        current_sprite_location = list(
            range(start_sprite, start_sprite + len(self.sprite))
        )
        # Screen index runs from
        #   0 to self.screen_rows * self.screen_pixels_per_row
        # However, the sprite location runs from
        #   0 to self.screen_pixels_per_row
        screen_idx = (self.clock - 1) % len(self.screen)
        col_idx = screen_idx % self.screen_pixels_per_row
        self.screen[screen_idx] = (
            self.pixel_on
            if col_idx in current_sprite_location
            else self.pixel_off
        )

    def draw_screen(self) -> None:
        """Draw screen"""
        for row_idx in range(self.screen_rows):
            row_start = row_idx * self.screen_pixels_per_row
            print(
                "".join(
                    self.screen[row_start : row_start + self.screen_pixels_per_row]
                )
            )

    def _evaluate_state(self):
        """The state of this processor should be evaluated at certain clock
        cycles"""
        if self.evaluate_clock_cycle(self.clock):
            self.evaluate_state()

    def _print_state(self):
        """The state of this processor should be printed at certain clock
        cycles"""
        if self.print_cycle(self.clock):
            self.draw_screen()


def relevant_clock_cycles(clock: int) -> bool:
    """Starting at clock cycle 20, every 40th clock cycle the internal processor
    state should be evaluated"""
    return (clock - 20) % 40 == 0


def part1(data: list[str]) -> int:
    """Advent of code 2022 day 10 - Part 1"""
    screen_processor = CathodeRayScreenProcessor(
        memory={'x': 1}, clock=1, evaluate_clock_cycle=relevant_clock_cycles,
        evaluate_state='signal_strength')
    for instruction in data:
        screen_processor.update(instruction)
    answer = screen_processor.total_signal_strength

    print(f"Solution day 10, part 1: {answer}")
    return answer


def should_draw_pixel(clock: int) -> bool:
    """Select the clock cycles at which to draw pixels (all cycles in this
    example)"""
    return True


def print_all_steps(clock: int) -> bool:
    """Print the screen for each clock cycle of the screen processor"""
    return False


def part2(data: list[str]) -> None:
    """Advent of code 2022 day 10 - Part 2"""
    screen_processor = CathodeRayScreenProcessor(
        memory={'x': 1}, clock=1, evaluate_clock_cycle=should_draw_pixel,
        evaluate_state='draw', print_cycle=print_all_steps
    )
    for instruction in data:
        screen_processor.update(instruction)
    screen_processor.draw_screen()
    answer = 0

    print(f"Solution day 10, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False, load_test_data: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
        load_test_data: Set to True if you want to load test data instead of
                        the full input. By default, this will load the file
                        called 'input10.1'
    """
    data = parse_data(load_test_data=load_test_data)

    for part in parts:
        if part == "a":
            aocd_result = part1(data)
        elif part == "b":
            aocd_result = part2(data)
        else:
            raise ValueError(f"Wrong part chosen, expecting 'a' or 'b': got {part}")

        if should_submit:
            submit(aocd_result, part=part, day=10, year=2022)


if __name__ == "__main__":
    test_data = False
    # test_data = True
    submit_answer = False
    # submit_answer = True
    # main("a", should_submit=submit_answer, load_test_data=test_data)
    # main("b", should_submit=submit_answer, load_test_data=test_data)
    main("ab", should_submit=submit_answer, load_test_data=test_data)
