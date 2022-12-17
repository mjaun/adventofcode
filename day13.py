from __future__ import annotations

import sys

from enum import Enum, auto
from typing import Union, List, Tuple

PacketItem = Union[int, List['PacketItem']]
Packet = List[PacketItem]


def main():
    result = 0
    for index, pair in enumerate(read_input_pairs()):
        if compare_packets(pair[0], pair[1]) == CompareResult.CORRECT_ORDER:
            result += (index + 1)
    print(result)


def compare_packets(lhs: Packet, rhs: Packet) -> CompareResult:
    for i in range(min(len(lhs), len(rhs))):
        result = compare_items(lhs[i], rhs[i])
        if result != CompareResult.CONTINUE:
            return result

    if len(lhs) < len(rhs):
        return CompareResult.CORRECT_ORDER
    elif len(lhs) > len(rhs):
        return CompareResult.WRONG_ORDER
    else:
        return CompareResult.CONTINUE


def compare_items(lhs: PacketItem, rhs: PacketItem):
    if type(lhs) == int and type(rhs) == int:
        return compare_integers(lhs, rhs)

    if type(lhs) == list and type(rhs) == list:
        return compare_packets(lhs, rhs)

    if type(lhs) == int and type(rhs) == list:
        return compare_packets([lhs], rhs)

    if type(lhs) == list and type(rhs) == int:
        return compare_packets(lhs, [rhs])

    raise NotImplementedError()


def compare_integers(lhs: int, rhs: int) -> CompareResult:
    if lhs < rhs:
        return CompareResult.CORRECT_ORDER
    elif lhs > rhs:
        return CompareResult.WRONG_ORDER
    else:
        return CompareResult.CONTINUE


class CompareResult(Enum):
    CORRECT_ORDER = auto()
    WRONG_ORDER = auto()
    CONTINUE = auto()


def read_input_pairs() -> List[Tuple[Packet, Packet]]:
    pairs = []
    lines = [line.strip() for line in sys.stdin.readlines()]

    for i in range(0, len(lines), 3):
        assert len(lines) <= i + 2 or lines[i + 2] == ''
        pairs.append((eval(lines[i]), eval(lines[i + 1])))

    return pairs


if __name__ == '__main__':
    main()
