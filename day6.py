import sys


def main():
    parser = ProtocolParser()

    for char in sys.stdin.read():
        parser.put_char(char)

        if parser.marker_detected:
            print(parser.index)
            break


class ProtocolParser:
    MARKER_SIZE = 4

    def __init__(self):
        self.index = 0
        self.marker_detected = False
        self.marker_buffer = ''

    def put_char(self, char: str):
        assert len(char) == 1

        self.index += 1

        if len(self.marker_buffer) < ProtocolParser.MARKER_SIZE:
            self.marker_buffer += char
        else:
            self.marker_buffer = self.marker_buffer[1:] + char

        if len(set(self.marker_buffer)) == ProtocolParser.MARKER_SIZE:
            self.marker_detected = True


if __name__ == '__main__':
    main()
