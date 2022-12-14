import sys

from typing import List


def main():
    elves = [Elf(input_lines) for input_lines in read_input_groups()]

    # part one
    elf_with_most_snacks = max(elves, key=lambda elf: elf.total_snacks())
    print(elf_with_most_snacks.total_snacks())

    # part two
    elves.sort(key=lambda elf: elf.total_snacks())
    top_three_elves = elves[-3:]
    print(sum(elf.total_snacks() for elf in top_three_elves))


class Elf:
    def __init__(self, input_lines: List[str]):
        self.snacks = [int(line) for line in input_lines]

    def total_snacks(self) -> int:
        return sum(self.snacks)


def read_input_groups() -> List[List[str]]:
    groups: List[List[str]] = []
    current_group: List[str] = []

    for line in sys.stdin.readlines():
        line = line.strip()
        if not line:
            groups.append(current_group)
            current_group = []
        else:
            current_group.append(line)

    return groups


if __name__ == '__main__':
    main()
