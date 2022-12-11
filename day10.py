from __future__ import annotations

import sys

from typing import NamedTuple, List, Optional, Dict


def main():
    cpu = Cpu()

    for line in read_input_lines():
        cpu.execute_instruction(line)

    print(sum(cpu.signal_strength(cycle_number) for cycle_number in range(20, 221, 40)))


class Cpu:
    def __init__(self):
        self.registerX = 1

        self._signal_strength_history = [1]

        self._instructions: Dict[str, CpuInstruction] = {
            'noop': NoopInstruction(self),
            'addx': AddXInstruction(self),
        }

    def execute_instruction(self, instruction_line: str):
        parts = instruction_line.split()
        self._instructions[parts[0]].execute(parts[1:])

    def signal_strength(self, cycle_number: int):
        return self._signal_strength_history[cycle_number - 1]

    def cycle_executed(self):
        cycle_number = len(self._signal_strength_history) + 1
        self._signal_strength_history.append(self.registerX * cycle_number)


class CpuState(NamedTuple):
    x: int


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
        self.cpu.registerX += int(args[0])
        self.cpu.cycle_executed()


def read_input_lines() -> List[str]:
    return [line.strip() for line in sys.stdin.readlines()]


if __name__ == '__main__':
    main()
