from __future__ import annotations

from enum import IntEnum

from day2_part1 import read_input_pairs


def main():
    total_score = 0

    for opponent_key, result_key in read_input_pairs():
        opponent_choice = RockPaperScissorChoice.from_encrypted_strategy_guide(opponent_key)
        round_result = RoundResult.from_encrypted_strategy_guide(result_key)

        player_choice = opponent_choice.find_choice_to(round_result)
        print(f'{opponent_key} {result_key} -> {opponent_choice} {player_choice}')
        total_score += get_round_score(player_choice, round_result)

    print(total_score)


def get_round_score(player_choice: RockPaperScissorChoice, round_result: RoundResult) -> int:
    choice_score = int(player_choice)
    round_score = int(round_result)
    return round_score + choice_score


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
        }

        return key_table[key]

    def find_choice_to(self, result: RoundResult):
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

        return lookup_table[result][self]


if __name__ == '__main__':
    main()
