from __future__ import annotations

import math
import sys

from enum import Enum, auto
from typing import List, NamedTuple, Dict, Iterable, Optional, Set, Tuple


def main():
    height_map, start_pos, end_pos = parse_input_lines(read_input_lines())

    # part one
    if path := a_star_algorithm(height_map, start_pos, end_pos):
        print(len(path) - 1)

    # part two
    path_lengths = []

    for position, height in height_map.items():
        if height != 0:
            continue

        if path := a_star_algorithm(height_map, position, end_pos):
            path_lengths.append(len(path) - 1)

    print(min(path_lengths))


def a_star_algorithm(height_map: HeightMap, start_pos: Position, end_pos: Position) -> Optional[Path]:
    # The heuristic function estimates the cost from a position to the end position.
    def heuristic_function(position: Position) -> float:
        return math.sqrt((end_pos.x - position.x) ** 2 + (end_pos.y - position.y) ** 2)

    # Looks up the preceding position of the cheapest currently known path from the start to a given position.
    came_from: Dict[Position, Position] = {}

    # The g-score is the cost of the cheapest currently known path from start to a given position.
    g_scores: Dict[Position, float] = {}

    # The f-score is the estimated cost of how cheap a path could be from start to finish if it goes through a given position.
    f_scores: Dict[Position, float] = {}

    # Set of discovered positions from where to look further. The positions are prioritized by their f-score.
    open_set: Set[Position] = set()

    def construct_path() -> Path:
        """ Constructs the final path given the information in came_from. """
        path = [end_pos]
        current_pos = end_pos

        while current_pos in came_from:
            current_pos = came_from[current_pos]
            path.insert(0, current_pos)

        return path

    def next_positions(position: Position) -> Iterable[Position]:
        """ Returns possible next positions from a given position. """
        current_height = height_map[position]

        for direction in Direction:
            next_position = position.next(direction)

            if next_position not in height_map:
                continue
            if height_map[next_position] > current_height + 1:
                continue

            yield next_position

    g_scores[start_pos] = 0
    f_scores[start_pos] = heuristic_function(start_pos)
    open_set.add(start_pos)

    while open_set:
        current_pos = min(open_set, key=lambda pos: f_scores[pos])
        open_set.remove(current_pos)

        if current_pos == end_pos:
            return construct_path()

        for next_pos in next_positions(current_pos):
            tentative_g_score = g_scores[current_pos] + 1

            if tentative_g_score < g_scores.get(next_pos, math.inf):
                came_from[next_pos] = current_pos
                g_scores[next_pos] = tentative_g_score
                f_scores[next_pos] = tentative_g_score + heuristic_function(next_pos)
                open_set.add(next_pos)

    return None


class Position(NamedTuple):
    x: int
    y: int

    def next(self, direction: Direction):
        method_map = {
            Direction.UP: lambda: Position(self.x, self.y - 1),
            Direction.DOWN: lambda: Position(self.x, self.y + 1),
            Direction.LEFT: lambda: Position(self.x - 1, self.y),
            Direction.RIGHT: lambda: Position(self.x + 1, self.y),
        }

        return method_map[direction]()


Path = List[Position]
HeightMap = Dict[Position, int]


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


def parse_input_lines(input_lines: List[str]) -> Tuple[HeightMap, Position, Position]:
    height_map: HeightMap = {}
    start_pos = Position(0, 0)
    end_pos = Position(0, 0)

    def height_from_letter(letter: str):
        assert len(letter) == 1 and letter.isalpha() and letter.islower()
        return ord(letter) - ord('a')

    for y, input_line in enumerate(input_lines):
        for x, letter in enumerate(input_line):
            current_pos = Position(x, y)

            if letter == 'S':
                start_pos = current_pos
                height = height_from_letter('a')
            elif letter == 'E':
                end_pos = current_pos
                height = height_from_letter('z')
            else:
                height = height_from_letter(letter)

            height_map[current_pos] = height

    return height_map, start_pos, end_pos


def read_input_lines() -> List[str]:
    return [line.strip() for line in sys.stdin.readlines()]


if __name__ == '__main__':
    main()
