from __future__ import annotations

import sys
from typing import Set


def main():
    rucksacks = [Rucksack(line) for line in read_input_lines()]
    priority_sum = 0

    for rucksack in rucksacks:
        for common_item in rucksack.get_common_items_in_both_departments():
            priority_sum += common_item.priority()

    print(priority_sum)


class Rucksack:
    def __init__(self, input_line: str):
        assert len(input_line) % 2 == 0
        middle_index = int(len(input_line) / 2)

        self.compartment1 = [Item(key) for key in input_line[:middle_index]]
        self.compartment2 = [Item(key) for key in input_line[middle_index:]]

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


def read_input_lines():
    return (line.strip() for line in sys.stdin.readlines())


if __name__ == '__main__':
    main()
