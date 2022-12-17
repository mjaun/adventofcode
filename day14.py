from __future__ import annotations

import sys

from enum import Flag, auto, Enum
from typing import NamedTuple, List, Dict, Optional


def main():
    rock_paths = read_input()

    # part one
    material_map = MaterialMap(rock_paths)
    sand_units = 0

    while position := material_map.pour_sand():
        if position.y > material_map.lowest_rock_y:
            break

        sand_units += 1

    print(sand_units)

    # part two
    material_map = MaterialMap(rock_paths)
    sand_units = 0

    while position := material_map.pour_sand():
        sand_units += 1

    print(sand_units)



class MaterialMap:
    def __init__(self, rock_paths: List[Path]):
        self.materials: Dict[Position, Material] = {}

        def fill_rock_line(from_position: Position, to_position: Position):
            current_position = from_position
            self.materials[current_position] = Material.ROCK

            while current_position != to_position:
                direction = current_position.direction_to(to_position)
                current_position = current_position.next(direction)
                self.materials[current_position] = Material.ROCK

        for rock_path in rock_paths:
            for i in range(len(rock_path) - 1):
                fill_rock_line(rock_path[i], rock_path[i + 1])

        self.lowest_rock_y = max(position.y for position in self.materials.keys())
        self.floor_y = self.lowest_rock_y + 2

    def pour_sand(self) -> Optional[Position]:
        current_position = Position(500, 0)

        if current_position in self.materials:
            return None

        while True:
            directions = [Direction.DOWN, Direction.DOWN | Direction.LEFT, Direction.DOWN | Direction.RIGHT]
            next_positions = (current_position.next(direction) for direction in directions)
            next_position = next(filter(lambda position: position not in self.materials, next_positions), None)

            if not next_position or next_position.y == self.floor_y:
                self.materials[current_position] = Material.SAND
                return current_position

            current_position = next_position


class Material(Enum):
    ROCK = auto()
    SAND = auto()


class Position(NamedTuple):
    x: int
    y: int

    @staticmethod
    def from_string(string: str):
        parts = string.split(',')
        assert len(parts) == 2
        return Position(int(parts[0]), int(parts[1]))

    def next(self, direction: Direction) -> Position:
        new_x = self.x
        new_y = self.y

        if direction & Direction.UP:
            new_y -= 1
        if direction & Direction.RIGHT:
            new_x += 1
        if direction & Direction.DOWN:
            new_y += 1
        if direction & Direction.LEFT:
            new_x -= 1

        return Position(new_x, new_y)

    def direction_to(self, other: Position) -> Direction:
        result = Direction.NONE

        if other.y < self.y:
            result |= Direction.UP
        if other.x > self.x:
            result |= Direction.RIGHT
        if other.y > self.y:
            result |= Direction.DOWN
        if other.x < self.x:
            result |= Direction.LEFT

        return result


Path = List[Position]


class Direction(Flag):
    NONE = 0
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


def read_input() -> List[Path]:
    result = []

    for line in sys.stdin.readlines():
        result.append([Position.from_string(s) for s in line.strip().split(' -> ')])

    return result


if __name__ == '__main__':
    main()
