from common_aoc import read_file_n

signal = read_file_n(6)[0]

PACKET_START_WIDTH = 4
MESSAGE_START_WIDTH = 14


def find_start_of_x(width: int) -> int:
    for i in range(width, len(signal)):
        if len(set(signal[i-width:i])) == width:
            return i


print(find_start_of_x(PACKET_START_WIDTH))
print(find_start_of_x(MESSAGE_START_WIDTH))
