from __future__ import annotations

import sys
from typing import Set, List, Generator, Iterable


def main():
    input_lines = read_input_lines()

    # part one
    rucksacks = [Rucksack(line) for line in input_lines]
    priority_sum = 0

    for rucksack in rucksacks:
        for common_item in rucksack.get_common_items_in_both_departments():
            priority_sum += common_item.priority()

    print(priority_sum)

    # part two
    elf_groups = [ElfGroup(lines) for lines in group_lines(input_lines, group_size=3)]
    priority_sum = 0

    for elf_group in elf_groups:
        for common_item in elf_group.get_common_items_in_all_rucksacks():
            priority_sum += common_item.priority()

    print(priority_sum)


class ElfGroup:
    def __init__(self, input_lines: List[str]):
        self.rucksacks = [Rucksack(line) for line in input_lines]

    def get_common_items_in_all_rucksacks(self) -> Set[Item]:
        result: Set[Item] = set(self.rucksacks[0].items())

        for rucksack in self.rucksacks[1:]:
            result = result & set(rucksack.items())

        return result


class Rucksack:
    def __init__(self, input_line: str):
        assert len(input_line) % 2 == 0
        middle_index = int(len(input_line) / 2)

        self.compartment1 = [Item(key) for key in input_line[:middle_index]]
        self.compartment2 = [Item(key) for key in input_line[middle_index:]]

    def items(self) -> Iterable[Item]:
        yield from self.compartment1
        yield from self.compartment2

    def get_common_items_in_both_departments(self) -> Set[Item]:
        return set(self.compartment1) & set(self.compartment2)


class Item:
    def __init__(self, key: str):
        assert len(key) == 1
        assert key.isalpha()
        self.key = key

    def priority(self) -> int:
        if self.key.isupper():
            return ord(self.key) - ord('A') + 27
        else:
            return ord(self.key) - ord('a') + 1

    def __eq__(self, other: Item):
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)


def group_lines(input_lines: List[str], group_size: int) -> Generator[List[str]]:
    assert len(input_lines) % group_size == 0

    for i in range(0, len(input_lines), group_size):
        yield input_lines[i:i + group_size]


def read_input_lines() -> List[str]:
    return [line.strip() for line in sys.stdin.readlines()]


if __name__ == '__main__':
    main()
