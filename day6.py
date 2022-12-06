import sys


def main():
    input_data = sys.stdin.read()

    # part one
    parser = ProtocolParser(marker_size=4)

    for char in input_data:
        parser.put_char(char)

        if parser.marker_detected:
            print(parser.index)
            break

    # part two
    parser = ProtocolParser(marker_size=14)

    for char in input_data:
        parser.put_char(char)

        if parser.marker_detected:
            print(parser.index)
            break


class ProtocolParser:
    def __init__(self, marker_size: int):
        self.index = 0
        self.marker_detected = False
        self.marker_buffer = ''
        self.marker_size = marker_size

    def put_char(self, char: str):
        assert len(char) == 1

        self.index += 1

        if len(self.marker_buffer) < self.marker_size:
            self.marker_buffer += char
        else:
            self.marker_buffer = self.marker_buffer[1:] + char

        if len(set(self.marker_buffer)) == self.marker_size:
            self.marker_detected = True


if __name__ == '__main__':
    main()
