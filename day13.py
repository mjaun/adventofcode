from __future__ import annotations

import functools
import sys

from enum import IntEnum
from typing import Union, List, Iterable

PacketItem = Union[int, List['PacketItem']]
Packet = List[PacketItem]


def main():
    packets = list(read_input_packets())

    # part one
    result = 0
    for i in range(int(len(packets) / 2)):
        if compare_packets(packets[i * 2], packets[i * 2 + 1]) == CompareResult.CORRECT_ORDER:
            result += i + 1
    print(result)

    # part two
    divider_packets = [[[2]], [[6]]]
    packets.extend(divider_packets)
    sort_packets(packets)
    divider_indexes = [i + 1 for i, packet in enumerate(packets) if packet in divider_packets]
    print(divider_indexes[0] * divider_indexes[1])

def sort_packets(packets: List[Packet]):
    packets.sort(key=functools.cmp_to_key(compare_packets))


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


class CompareResult(IntEnum):
    CORRECT_ORDER = -1
    WRONG_ORDER = 1
    CONTINUE = 0


def read_input_packets() -> Iterable[Packet, Packet]:
    lines = [line.strip() for line in sys.stdin.readlines()]

    for i in range(0, len(lines), 3):
        assert len(lines) <= i + 2 or lines[i + 2] == ''
        yield eval(lines[i])
        yield eval(lines[i + 1])


if __name__ == '__main__':
    main()
