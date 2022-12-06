import re

from aocd import get_data, submit


def evaluate_round(opponent_move: str, player_move: str) -> int:
    """Evaluate the result of a rock-paper-scissors round, from the perspective
    of the player.
    X or A: rock
    Y or B: paper
    Z or C: scissors
    """
    if (
        (player_move == "X" and opponent_move == "C")
        or (player_move == "Y" and opponent_move == "A")
        or (player_move == "Z" and opponent_move == "B")
    ):
        # player wins
        return 6
    elif (
        (player_move == "X" and opponent_move == "A")
        or (player_move == "Y" and opponent_move == "B")
        or (player_move == "Z" and opponent_move == "C")
    ):
        # draw
        return 3
    else:
        # player loses
        return 0


def evaluate_move(opponent_move: str, round_result: str) -> str:
    """Evaluate the move that the player should select to achieve the expected
    result for a rock-paper-scissors round.
    X or A: rock
    Y or B: paper
    Z or C: scissors
    X: lose
    Y: draw
    Z: win
    """
    if opponent_move == "A":
        result_scheme = {
            "X": "Z",
            "Y": "X",
            "Z": "Y",
        }
    elif opponent_move == "B":
        result_scheme = {
            "X": "X",
            "Y": "Y",
            "Z": "Z",
        }
    elif opponent_move == "C":
        result_scheme = {
            "X": "Y",
            "Y": "Z",
            "Z": "X",
        }
    else:
        raise ValueError(
            f"Invalid opponent move, expected A, B, or C, got {opponent_move}"
        )
    return result_scheme[round_result]


def move_score(player_move: str) -> int:
    """Determine the score for the move that the player chosen"""
    scoring_scheme = {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }
    if player_move not in scoring_scheme:
        raise ValueError(
            f"Invalid move chosen, expected X, Y, or Z but got {player_move}"
        )
    return scoring_scheme[player_move]


def parse_data() -> dict[str, list[str]]:
    """Parser function to parse today's data"""
    data = get_data(day=2, year=2022)
    # with open("input2.1", "r") as f:
    #     data = f.read()
    moves = re.findall("\S", data)
    parsed_data = {"opponent_moves": moves[::2], "player_moves": moves[1::2]}
    # lines = data.splitlines()
    # numbers = [int(x) for x in re.findall("(-?\d+)", data)]
    return parsed_data


def part1(data: dict[str, list[str]]) -> int:
    """Advent of code 2022 day 2 - Part 1"""
    answer = 0
    for opponent_move, player_move in zip(data["opponent_moves"], data["player_moves"]):
        result_score = evaluate_round(opponent_move, player_move)
        player_move_score = move_score(player_move)
        answer += player_move_score + result_score

    print(f"Solution day 2, part 1: {answer}")
    return answer


def part2(data: dict[str, list[str]]) -> int:
    """Advent of code 2022 day 2 - Part 2"""
    answer = 0
    for opponent_move, round_result in zip(
        data["opponent_moves"], data["player_moves"]
    ):
        player_move = evaluate_move(opponent_move, round_result)
        result_score = evaluate_round(opponent_move, player_move)
        player_move_score = move_score(player_move)
        answer += player_move_score + result_score

    print(f"Solution day 2, part 2: {answer}")
    return answer


def main(parts: str, should_submit: bool = False) -> None:
    """Main function for solving the selected part(s) of today's puzzle
    and automatically submitting the answer.

    Args:
        parts:          "a", "b", or "ab". Execute the chosen parts
        should_submit:  Set to True if you want to submit your answer
    """
    data = parse_data()

    for part in parts:
        if part == "a":
            aocd_result = part1(data)
        elif part == "b":
            aocd_result = part2(data)
        else:
            raise ValueError(f"Wrong part chosen, expecting 'a' or 'b': got {part}")

        if should_submit:
            submit(aocd_result, part=part, day=2, year=2022)


if __name__ == "__main__":
    submit_answer = False
    # submit_answer = True
    # main("a", submit_answer)
    # main("b", submit_answer)
    main("ab", submit_answer)
