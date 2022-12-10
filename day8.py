from __future__ import annotations

import sys
from enum import Enum

from typing import Dict, List, Iterable


def main():
    input_lines = read_input_lines()
    forest = parse_input_lines(input_lines)

    print(sum(1 for tree in forest.trees if forest.is_visible(tree)))


class Forest:
    def __init__(self):
        self.trees: Dict[Position, Tree] = {}

    def add_tree(self, tree: Tree):
        self.trees[tree.position] = tree

    def is_visible(self, position: Position) -> bool:
        tree = self.trees[position]

        def trees_in_direction(direction: Direction) -> Iterable[Tree]:
            next_position = tree.position.next(direction)
            while next_position in self.trees:
                yield self.trees[next_position]
                next_position = next_position.next(direction)

        def visible_in_direction(direction: Direction) -> bool:
            return not any(neighbour_tree.height >= tree.height for neighbour_tree in trees_in_direction(direction))

        return any(visible_in_direction(direction) for direction in Direction)


class Tree:
    def __init__(self, position: Position, height: int):
        self.position = position
        self.height = height


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def next(self, direction: Direction):
        method_map = {
            Direction.UP: lambda: Position(self.x, self.y - 1),
            Direction.DOWN: lambda: Position(self.x, self.y + 1),
            Direction.LEFT: lambda: Position(self.x - 1, self.y),
            Direction.RIGHT: lambda: Position(self.x + 1, self.y),
        }

        return method_map[direction]()

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __repr__(self):
        return str((self.x, self.y))


def parse_input_lines(input_lines: List[str]) -> Forest:
    forest = Forest()

    for y, line in enumerate(input_lines):
        for x, height in enumerate(line):
            forest.add_tree(Tree(Position(x, y), height))

    return forest


def read_input_lines() -> List[str]:
    return [line.strip() for line in sys.stdin.readlines()]


if __name__ == '__main__':
    main()
