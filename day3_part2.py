from __future__ import annotations

import sys
from typing import Set, List, Generator

from day3_part1 import Item


def main():
    elf_groups = [ElfGroup(lines) for lines in read_input_grouped(group_size=3)]
    priority_sum = 0

    for elf_group in elf_groups:
        for common_item in elf_group.get_common_items_in_all_rucksacks():
            priority_sum += common_item.priority()

    print(priority_sum)


class ElfGroup:
    def __init__(self, input_lines: List[str]):
        self.rucksacks = [Rucksack(line) for line in input_lines]

    def get_common_items_in_all_rucksacks(self) -> Set[Item]:
        result: Set[Item] = set(self.rucksacks[0].items)

        for rucksack in self.rucksacks[1:]:
            result = result & set(rucksack.items)

        return result


class Rucksack:
    def __init__(self, input_line: str):
        self.items = [Item(key) for key in input_line]


def read_input_grouped(group_size: int) -> Generator[List[str]]:
    input_lines = list(read_input_lines())
    assert len(input_lines) % group_size == 0

    for i in range(0, len(input_lines), group_size):
        yield input_lines[i:i + group_size]


def read_input_lines() -> Generator[str]:
    return (line.strip() for line in sys.stdin.readlines())


if __name__ == '__main__':
    main()
