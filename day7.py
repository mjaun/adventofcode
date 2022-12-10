from __future__ import annotations

import os
import sys

from typing import List, Dict, Iterable


def main():
    file_system = FileSystem()
    parser = ConsoleOutputParser(file_system)

    for input_line in read_input_lines():
        parser.process_line(input_line)
    parser.finish_command()

    # part one
    all_directories = file_system.root_directory.iterate_subdirectories_recursively()
    print(sum(d.get_total_size() for d in all_directories if d.get_total_size() <= 100000))

    # part two
    total_space = 70000000
    space_needed = 30000000
    space_used = file_system.root_directory.get_total_size()
    space_to_free = space_used + space_needed - total_space
    assert space_to_free > 0

    all_directories = file_system.root_directory.iterate_subdirectories_recursively()
    print(min(d.get_total_size() for d in all_directories if d.get_total_size() >= space_to_free))


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name: str):
        self.name = name
        self.files: Dict[str, File] = {}
        self.directories: Dict[str, Directory] = {}

    def create_subdirectory(self, path: str) -> Directory:
        parts = path.split('/')
        directory_name = parts[0]

        if directory_name not in self.directories:
            self.directories[directory_name] = Directory(directory_name)

        directory = self.directories[directory_name]

        if len(parts) == 1:
            return directory
        else:
            return directory.create_subdirectory('/'.join(parts[1:]))

    def add_file(self, file: File):
        if file.name in self.files:
            del self.files[file.name]

        self.files[file.name] = file

    def get_total_size(self) -> int:
        total_size = 0

        for directory in self.directories.values():
            total_size += directory.get_total_size()

        for file in self.files.values():
            total_size += file.size

        return total_size

    def iterate_subdirectories_recursively(self) -> Iterable[Directory]:
        for subdirectory in self.directories.values():
            yield subdirectory
            yield from subdirectory.iterate_subdirectories_recursively()


class FileSystem:
    def __init__(self):
        self.current_path = '/'
        self.root_directory = Directory('')

    def change_directory(self, path: str):
        self.current_path = os.path.normpath(os.path.join(self.current_path, path))

    def get_current_directory(self) -> Directory:
        return self.root_directory.create_subdirectory(self.current_path[1:])


class CommandParser:
    def __init__(self, file_system: FileSystem):
        self.file_system = file_system

    def parse(self, arguments: List[str], output_lines: List[str]):
        raise NotImplementedError()


class ChangeDirectoryCommandParser(CommandParser):
    def parse(self, arguments: List[str], output_lines: List[str]):
        assert len(arguments) == 1
        assert len(output_lines) == 0

        self.file_system.change_directory(arguments[0])


class ListDirectoryCommandParser(CommandParser):
    def parse(self, arguments: List[str], output_lines: List[str]):
        assert len(arguments) == 0

        current_directory = self.file_system.get_current_directory()

        for output_line in output_lines:
            parts = output_line.split()
            assert len(parts) == 2

            # we don't care about directories as they are created on the fly
            if parts[0] == 'dir':
                continue

            current_directory.add_file(File(name=parts[1], size=int(parts[0])))


class ConsoleOutputParser:
    def __init__(self, file_system: FileSystem):
        self.current_command = ''
        self.current_output: List[str] = []

        self.command_parsers: Dict[str, CommandParser] = {
            'cd': ChangeDirectoryCommandParser(file_system),
            'ls': ListDirectoryCommandParser(file_system),
        }

    def process_line(self, line: str):
        if line.startswith('$'):
            self.finish_command()

            self.current_command = line[2:]
            self.current_output = []
        else:
            self.current_output.append(line)

    def finish_command(self):
        if self.current_command:
            self.parse_command(self.current_command, self.current_output)

    def parse_command(self, command: str, output_lines: List[str]):
        parts = command.split()
        executable = parts[0]
        arguments = parts[1:]

        self.command_parsers[executable].parse(arguments, output_lines)


def read_input_lines() -> List[str]:
    return [line.strip() for line in sys.stdin.readlines()]


if __name__ == '__main__':
    main()
