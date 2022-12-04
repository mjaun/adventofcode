from day1_part1 import initialize_elves


def main():
    elves = initialize_elves()

    elves.sort(key=lambda elf: elf.total_snacks())
    top_three_elves = elves[-3:]

    print(sum(elf.total_snacks() for elf in top_three_elves))


if __name__ == '__main__':
    main()
