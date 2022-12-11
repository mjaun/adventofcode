from __future__ import annotations

import re
import sys
import math

from typing import Callable, List, Iterable, NamedTuple


def main():
    input_groups = list(read_input_groups())

    # part one
    monkeys = [Monkey.from_input_lines(input_group) for input_group in input_groups]
    dispatcher = Dispatcher(monkeys)

    for _ in range(20):
        dispatcher.execute_round()

    print(dispatcher.monkey_business_level())

    # part two
    monkeys = [Monkey.from_input_lines(input_group) for input_group in input_groups]
    dispatcher = Dispatcher(monkeys)

    Monkey.worry_levels_divisor = 0  # disable
    Monkey.worry_levels_modulo = math.lcm(*[monkey.test_divisor for monkey in monkeys])  # requires Python 3.9

    for i in range(10000):
        dispatcher.execute_round()

    print(dispatcher.monkey_business_level())


class Dispatcher:
    def __init__(self, monkeys: List[Monkey]):
        self.monkeys = monkeys

    def execute_round(self):
        for monkey in self.monkeys:
            self.execute_turn(monkey)

    def execute_turn(self, monkey: Monkey):
        for item, target_index in monkey.execute_turn():
            self.monkeys[target_index].items.append(item)

    def monkey_business_level(self) -> int:
        monkeys_sorted = sorted(self.monkeys, key=lambda monkey: monkey.inspect_count, reverse=True)
        return monkeys_sorted[0].inspect_count * monkeys_sorted[1].inspect_count


class Monkey:
    worry_levels_divisor = 3
    worry_levels_modulo = 0

    @staticmethod
    def from_input_lines(input_lines: List[str]):
        assert re.match('^Monkey [0-9]+:$', input_lines[0])
        starting_items = re.match('^Starting items: ([0-9, ]+)$', input_lines[1])
        operation = re.match('^Operation: new = (.*)$', input_lines[2])
        test_divisor = re.match('^Test: divisible by ([0-9]+)$', input_lines[3])
        test_true_index = re.match('^If true: throw to monkey ([0-9]+)$', input_lines[4])
        test_false_index = re.match('^If false: throw to monkey ([0-9]+)$', input_lines[5])

        monkey = Monkey()
        monkey.items = [Item(int(value_str)) for value_str in starting_items.group(1).split(', ')]
        monkey.operation = create_operation(operation.group(1))
        monkey.test_divisor = int(test_divisor.group(1))
        monkey.test_true_index = int(test_true_index.group(1))
        monkey.test_false_index = int(test_false_index.group(1))
        return monkey

    def __init__(self):
        self.items: List[Item] = []
        self.operation: Callable[[Item], None] = lambda item: None
        self.test_divisor = 0
        self.test_true_index = 0
        self.test_false_index = 0
        self.inspect_count = 0

    def execute_turn(self) -> Iterable[TurnResult]:
        while self.items:
            self.inspect_count += 1

            item = self.items.pop(0)
            self.operation(item)

            if Monkey.worry_levels_divisor:
                item.worry_level = int(item.worry_level / Monkey.worry_levels_divisor)
            if Monkey.worry_levels_modulo:
                item.worry_level = item.worry_level % Monkey.worry_levels_modulo

            if value_divisible_by(item.worry_level, self.test_divisor):
                target_index = self.test_true_index
            else:
                target_index = self.test_false_index

            yield item, target_index


def create_operation(expression: str) -> Callable[[Item], None]:
    code = compile(expression, '<string>', 'eval')

    def operation(item: Item):
        item.worry_level = eval(code, {'old': item.worry_level})

    return operation


def value_divisible_by(value: int, divisor: int) -> bool:
    return value % divisor == 0


class TurnResult(NamedTuple):
    item: Item
    target_index: int


class Item:
    def __init__(self, worry_level: int):
        self.worry_level = worry_level

    def __repr__(self) -> str:
        return str(self.worry_level)


def read_input_groups() -> Iterable[List[str]]:
    current_group: List[str] = []

    for line in sys.stdin.readlines():
        line = line.strip()

        if not line:
            yield current_group
            current_group = []
        else:
            current_group.append(line)

    yield current_group


if __name__ == '__main__':
    main()
