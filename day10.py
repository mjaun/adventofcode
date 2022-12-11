from __future__ import annotations

import sys

from typing import NamedTuple, List, Optional, Dict


def main():
    cpu = Cpu()
    crt = Crt()

    cpu.on_cycle_executed = lambda: crt.draw_pixel(cpu.register_x)
    crt.draw_pixel(cpu.register_x)  # draw pixel for cycle 1

    for line in read_input_lines():
        cpu.execute_instruction(line)

    # part one
    print(sum(cpu.signal_strength(cycle_number) for cycle_number in range(20, 221, 40)))

    # part two
    crt.print()


class Cpu:
    def __init__(self):
        self.register_x = 1
        self.on_cycle_executed = lambda: None

        self.signal_strength_history = [1]

        self.instructions: Dict[str, CpuInstruction] = {
            'noop': NoopInstruction(self),
            'addx': AddXInstruction(self),
        }

    def execute_instruction(self, instruction_line: str):
        parts = instruction_line.split()
        self.instructions[parts[0]].execute(parts[1:])

    def signal_strength(self, cycle_number: int):
        return self.signal_strength_history[cycle_number - 1]

    def cycle_executed(self):
        cycle_number = len(self.signal_strength_history) + 1
        self.signal_strength_history.append(self.register_x * cycle_number)
        self.on_cycle_executed()


class CpuInstruction:
    def __init__(self, cpu: Cpu):
        self.cpu = cpu

    def execute(self, args: List[str]):
        raise NotImplementedError()


class NoopInstruction(CpuInstruction):
    def execute(self, args: List[str]):
        assert len(args) == 0

        self.cpu.cycle_executed()


class AddXInstruction(CpuInstruction):
    def execute(self, args: List[str]):
        assert len(args) == 1

        self.cpu.cycle_executed()
        self.cpu.register_x += int(args[0])
        self.cpu.cycle_executed()


class Crt:
    WIDTH = 40

    def __init__(self):
        self.output = ''
        self.cursor = 0

    def draw_pixel(self, sprite_position: int):
        column_index = self.cursor % Crt.WIDTH
        pixel_lit = column_index in range(sprite_position - 1, sprite_position + 2)
        self.output += '#' if pixel_lit else '.'

        if column_index == Crt.WIDTH - 1:
            self.output += '\n'

        self.cursor += 1

    def print(self):
        print(self.output)


def read_input_lines() -> List[str]:
    return [line.strip() for line in sys.stdin.readlines()]


if __name__ == '__main__':
    main()
