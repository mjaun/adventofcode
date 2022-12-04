from day1_part1 import Elf, read_input_groups


def main():
    elves = [Elf(input_lines) for input_lines in read_input_groups()]

    elves.sort(key=lambda elf: elf.total_snacks())
    top_three_elves = elves[-3:]

    print(sum(elf.total_snacks() for elf in top_three_elves))


if __name__ == '__main__':
    main()
