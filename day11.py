from __future__ import annotations

import re
import sys
from typing import Callable, List, Iterable, NamedTuple


def main():
    monkeys = [Monkey.from_input_lines(input_groups) for input_groups in read_input_groups()]
    dispatcher = Dispatcher(monkeys)

    for _ in range(20):
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
    @staticmethod
    def from_input_lines(input_lines: List[str]):
        assert re.match('^Monkey [0-9]+:$', input_lines[0])
        starting_items = re.match('^Starting items: ([0-9, ]+)$', input_lines[1])
        operation = re.match('^Operation: new = (\w+) (.) (\w+)$', input_lines[2])
        test = re.match('^Test: divisible by ([0-9]+)$', input_lines[3])
        if_true = re.match('^If true: throw to monkey ([0-9]+)$', input_lines[4])
        if_false = re.match('^If false: throw to monkey ([0-9]+)$', input_lines[5])

        monkey = Monkey()
        monkey.items = [Item(int(value_str)) for value_str in starting_items.group(1).split(', ')]
        monkey.operation = create_operation(operation.group(1), operation.group(2), operation.group(3))
        monkey.test = lambda item: item.worry_level % int(test.group(1)) == 0
        monkey.if_true_index = int(if_true.group(1))
        monkey.if_false_index = int(if_false.group(1))
        return monkey

    def __init__(self):
        self.items: List[Item] = []
        self.operation: Callable[[Item], None] = lambda item: None
        self.test: Callable[[Item], bool] = lambda _item: True
        self.if_true_index: int = 0
        self.if_false_index: int = 0
        self.inspect_count: int = 0

    def execute_turn(self) -> Iterable[TurnResult]:
        while self.items:
            self.inspect_count += 1

            item = self.items.pop(0)
            self.operation(item)
            item.worry_level = int(item.worry_level / 3)
            target_index = self.if_true_index if self.test(item) else self.if_false_index
            yield item, target_index


def create_operation(operand1: str, operator: str, operand2: str):
    def operation(item: Item):
        def parse_operand(operand: str) -> int:
            if operand == 'old':
                return item.worry_level

            return int(operand)

        operand1_parsed = parse_operand(operand1)
        operand2_parsed = parse_operand(operand2)

        operation_table = {
            '+': lambda: operand1_parsed + operand2_parsed,
            '*': lambda: operand1_parsed * operand2_parsed,
        }

        item.worry_level = operation_table[operator]()

    return operation


class TurnResult(NamedTuple):
    item: Item
    target_index: int


class Item:
    def __init__(self, worry_level: int):
        self.worry_level = worry_level

    def __repr__(self):
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
