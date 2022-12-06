from __future__ import annotations

import sys

from enum import IntEnum
from typing import List, Tuple


def main():
    input_pairs = read_input_pairs()

    # part one
    total_score = 0

    for opponent_key, player_key in input_pairs:
        player_choice = RockPaperScissorChoice.from_encrypted_strategy_guide(player_key)
        opponent_choice = RockPaperScissorChoice.from_encrypted_strategy_guide(opponent_key)

        round_result = get_round_result(player_choice, opponent_choice)
        total_score += get_round_score(player_choice, round_result)

    print(total_score)

    # part two
    total_score = 0

    for opponent_key, result_key in input_pairs:
        opponent_choice = RockPaperScissorChoice.from_encrypted_strategy_guide(opponent_key)
        round_result = RoundResult.from_encrypted_strategy_guide(result_key)

        player_choice = find_choice(opponent_choice, round_result)
        total_score += get_round_score(player_choice, round_result)

    print(total_score)


def get_round_result(player_choice: RockPaperScissorChoice, opponent_choice: RockPaperScissorChoice) -> int:
    if player_choice == find_choice(opponent_choice, RoundResult.WIN):
        return RoundResult.WIN
    elif player_choice == opponent_choice:
        return RoundResult.DRAW
    else:
        return RoundResult.LOSS


def get_round_score(player_choice: RockPaperScissorChoice, round_result: RoundResult) -> int:
    choice_score = int(player_choice)
    round_score = int(round_result)
    return round_score + choice_score

def find_choice(opponent_choice: RockPaperScissorChoice, result: RoundResult):
    lookup_table = {
        RoundResult.WIN: {
            RockPaperScissorChoice.ROCK: RockPaperScissorChoice.PAPER,
            RockPaperScissorChoice.PAPER: RockPaperScissorChoice.SCISSOR,
            RockPaperScissorChoice.SCISSOR: RockPaperScissorChoice.ROCK,
        },
        RoundResult.DRAW: {
            RockPaperScissorChoice.ROCK: RockPaperScissorChoice.ROCK,
            RockPaperScissorChoice.PAPER: RockPaperScissorChoice.PAPER,
            RockPaperScissorChoice.SCISSOR: RockPaperScissorChoice.SCISSOR,
        },
        RoundResult.LOSS: {
            RockPaperScissorChoice.ROCK: RockPaperScissorChoice.SCISSOR,
            RockPaperScissorChoice.PAPER: RockPaperScissorChoice.ROCK,
            RockPaperScissorChoice.SCISSOR: RockPaperScissorChoice.PAPER,
        },
    }

    return lookup_table[result][opponent_choice]


class RoundResult(IntEnum):
    WIN = 6
    DRAW = 3
    LOSS = 0

    @staticmethod
    def from_encrypted_strategy_guide(key: str) -> RoundResult:
        key_table = {
            'X': RoundResult.LOSS,
            'Y': RoundResult.DRAW,
            'Z': RoundResult.WIN,
        }

        return key_table[key]


class RockPaperScissorChoice(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3

    @staticmethod
    def from_encrypted_strategy_guide(key: str) -> RockPaperScissorChoice:
        key_table = {
            'A': RockPaperScissorChoice.ROCK,
            'B': RockPaperScissorChoice.PAPER,
            'C': RockPaperScissorChoice.SCISSOR,

            # for part one only
            'X': RockPaperScissorChoice.ROCK,
            'Y': RockPaperScissorChoice.PAPER,
            'Z': RockPaperScissorChoice.SCISSOR,
        }

        return key_table[key]


def read_input_pairs() -> List[Tuple[str, str]]:
    pairs: List[Tuple[str, str]] = []

    for line in sys.stdin.readlines():
        line = line.strip()
        pair = line.split()
        assert len(pair) == 2
        pairs.append((pair[0], pair[1]))

    return pairs


if __name__ == '__main__':
    main()
