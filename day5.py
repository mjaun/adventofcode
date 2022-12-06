from __future__ import annotations

import sys
import re

from typing import List, Tuple


def main():
    initial_state, instructions = read_input_sections()

    # part one
    cargo_depot = CargoDepot(initial_state)

    for instruction in instructions:
        cargo_depot.execute_instruction(instruction)

    print(cargo_depot.get_top_crates_encoded())

    # part two
    cargo_depot = CargoDepot(initial_state)
    cargo_depot.crane_moves_crates_in_order = True

    for instruction in instructions:
        cargo_depot.execute_instruction(instruction)

    print(cargo_depot.get_top_crates_encoded())


class CargoDepot:
    def __init__(self, initial_state: List[str]):
        self.stacks: List[List[Crate]] = []
        self.crane_moves_crates_in_order = False

        for line in reversed(initial_state):
            crate_keys = [line[i] for i in range(1, len(line), 4)]
            for stack_id, crate_key in enumerate(crate_keys):
                if crate_key == ' ':
                    continue
                self.put_crate(Crate(crate_key), stack_id)

    def execute_instruction(self, instruction: str):
        match = re.match('move ([0-9]+) from ([0-9]+) to ([0-9]+)', instruction)
        assert match

        self.execute_instruction_decoded(
            move_count=int(match.group(1)),
            from_stack_id=int(match.group(2)) - 1,
            to_stack_id=int(match.group(3)) - 1,
        )

    def execute_instruction_decoded(self, from_stack_id: int, to_stack_id: int, move_count: int):
        assert from_stack_id < len(self.stacks)
        assert len(self.stacks[from_stack_id]) >= move_count

        moved_crates = self.stacks[from_stack_id][-move_count:]

        if not self.crane_moves_crates_in_order:
            moved_crates.reverse()

        del self.stacks[from_stack_id][-move_count:]
        self.stacks[to_stack_id].extend(moved_crates)

    def put_crate(self, crate: Crate, stack_id: int):
        self.extend_stacks(stack_id)
        self.stacks[stack_id].append(crate)

    def extend_stacks(self, stack_id: int):
        while len(self.stacks) <= stack_id:
            self.stacks.append([])

    def get_top_crates_encoded(self):
        result = ''
        for stack in self.stacks:
            result += stack[-1].key if stack else ' '
        return result


class Crate:
    def __init__(self, key: str):
        assert len(key) == 1
        assert key.isalpha()
        self.key = key

    def __repr__(self):
        return self.key


def read_input_sections() -> Tuple[List[str], List[str]]:
    input_lines = [line.rstrip() for line in sys.stdin.readlines()]
    empty_indexes = [index for index, value in enumerate(input_lines) if not value]
    section_end = empty_indexes[0]
    return input_lines[:section_end - 1], input_lines[section_end + 1:]


if __name__ == '__main__':
    main()
