from __future__ import annotations

from typing import List

from day4_part1 import read_input_pairs


def main():
    result = 0

    for first_range, second_range in read_input_pairs():
        first_elf = Elf(first_range)
        second_elf = Elf(second_range)

        if Elf.have_overlapping_sections(first_elf, second_elf):
            result += 1

    print(result)


class Elf:
    def __init__(self, section_range: str):
        section_range_ids = [int(id_str) for id_str in section_range.split('-')]
        assert len(section_range_ids) == 2
        assert section_range_ids[0] <= section_range_ids[1]

        self.section_ids: List[int] = list(range(section_range_ids[0], section_range_ids[1] + 1))

    @staticmethod
    def have_overlapping_sections(first: Elf, second: Elf):
        common_sections = set(first.section_ids) & set(second.section_ids)
        return len(common_sections) > 0


if __name__ == '__main__':
    main()
