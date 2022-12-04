import sys

from typing import List, Iterable


def main():
    elves: List[Elf] = []

    for input_group in read_input_groups():
        elves.append(Elf(int(x) for x in input_group))

    elf_with_most_snacks = max(elves, key=lambda elf: elf.total_snacks())
    print(elf_with_most_snacks.total_snacks())


class Elf:
    def __init__(self, snacks: Iterable[int]):
        self.snacks = list(snacks)

    def total_snacks(self) -> int:
        return sum(self.snacks)


def initialize_elves() -> List[Elf]:
    elves: List[Elf] = []

    for input_group in read_input_groups():
        elves.append(Elf(int(x) for x in input_group))

    return elves


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
