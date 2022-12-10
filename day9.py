from __future__ import annotations

import sys

from enum import Flag, auto
from typing import List, Tuple, Set


def main():
    rope = Rope()
    tail_positions: Set[Position] = set()

    for direction, distance in read_input():
        for _ in range(distance):
            rope.move_head(direction)
            tail_positions.add(rope.tail_pos)

    print(len(tail_positions))


class Rope:
    def __init__(self):
        self.head_pos = Position(0, 0)
        self.tail_pos = Position(0, 0)

    def move_head(self, direction: Direction):
        self.head_pos = self.head_pos.next_in_direction(direction)
        self._tail_catch_up()

    def _tail_catch_up(self):
        delta = self.head_pos - self.tail_pos

        if abs(delta.x) > 1 or abs(delta.y) > 1:
            head_direction = self.tail_pos.direction_to(self.head_pos)
            self.tail_pos = self.tail_pos.next_in_direction(head_direction)


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def next_in_direction(self, direction: Direction) -> Position:
        dx = 0
        dy = 0

        if Direction.UP in direction:
            dy = 1
        if Direction.DOWN in direction:
            dy = -1
        if Direction.RIGHT in direction:
            dx = 1
        if Direction.LEFT in direction:
            dx = -1

        return self + Position(dx, dy)

    def direction_to(self, other: Position) -> Direction:
        delta = other - self
        direction = Direction.NONE

        if delta.x > 0:
            direction |= Direction.RIGHT
        if delta.x < 0:
            direction |= Direction.LEFT
        if delta.y > 0:
            direction |= Direction.UP
        if delta.y < 0:
            direction |= Direction.DOWN

        return direction

    def __add__(self, other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Position) -> Position:
        return Position(self.x - other.x, self.y - other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: Position) -> bool:
        return (self.x, self.y) == (other.x, other.y)

    def __repr__(self) -> str:
        return str((self.x, self.y))


class Direction(Flag):
    NONE = 0
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()

    @staticmethod
    def from_input_code(input_code: str):
        direction_map = {
            'U': Direction.UP,
            'R': Direction.RIGHT,
            'D': Direction.DOWN,
            'L': Direction.LEFT,
        }

        return direction_map[input_code]


def read_input() -> List[Tuple[Direction, int]]:
    result = []

    for line in sys.stdin.readlines():
        parts = line.strip().split()
        assert len(parts) == 2
        result.append((Direction.from_input_code(parts[0]), int(parts[1])))

    return result


if __name__ == '__main__':
    main()
