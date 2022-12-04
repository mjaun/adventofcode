from __future__ import annotations

import sys

from enum import IntEnum
from typing import List, Tuple


def main():
    total_score = 0

    for opponent_key, player_key in read_input_pairs():
        player_choice = RockPaperScissorChoice.from_encrypted_strategy_guide(player_key)
        opponent_choice = RockPaperScissorChoice.from_encrypted_strategy_guide(opponent_key)
        total_score += play_round(player_choice, opponent_choice)

    print(total_score)


def play_round(player_choice: RockPaperScissorChoice, opponent_choice: RockPaperScissorChoice) -> int:
    choice_score = int(player_choice)

    if player_choice.wins_against(opponent_choice):
        round_score = 6
    elif player_choice == opponent_choice:
        round_score = 3
    else:
        round_score = 0

    return round_score + choice_score


class RockPaperScissorChoice(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3

    @staticmethod
    def from_encrypted_strategy_guide(key: str):
        key_table = {
            'A': RockPaperScissorChoice.ROCK,
            'B': RockPaperScissorChoice.PAPER,
            'C': RockPaperScissorChoice.SCISSOR,
            'X': RockPaperScissorChoice.ROCK,
            'Y': RockPaperScissorChoice.PAPER,
            'Z': RockPaperScissorChoice.SCISSOR,
        }

        return key_table[key]

    def wins_against(self, other: RockPaperScissorChoice):
        winning_choice_table = {
            RockPaperScissorChoice.ROCK: RockPaperScissorChoice.SCISSOR,
            RockPaperScissorChoice.PAPER: RockPaperScissorChoice.ROCK,
            RockPaperScissorChoice.SCISSOR: RockPaperScissorChoice.PAPER,
        }

        return winning_choice_table[self] == other


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
