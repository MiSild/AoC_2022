from common_aoc import read_file_n
from re import findall


def get_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def no_beacons(x, y, y_r, manh, marks):
    x_width = manh - abs(y - y_r)
    if x_width >= 0:
        marks[f"{x}:{y_r}"] = '#'
        for x_i in range(1, x_width + 1):
            marks[f"{x + x_i}:{y_r}"] = '#'
            marks[f"{x - x_i}:{y_r}"] = '#'


def get_x_width(manh, y, y2):
    return manh - abs(y - y2)


sensors = read_file_n(15, "inputs", True)
cord_regex = '(?<=[xy]=)[^,:]*'
y_row = 10
marked = {}
x_beacons = {}
for sensor in sensors:
    s_x, s_y, b_x, b_y = [int(i) for i in findall(cord_regex, sensor)]
    if b_y == y_row:
        x_beacons[f"{b_x}:{b_y}"] = '#'
    manh = get_manhattan(s_x, s_y, b_x, b_y)
    no_beacons(s_x, s_y, y_row, manh, marked)

for key in x_beacons.keys():
    del marked[key]
print(len(marked.keys()))

x_ceil = 4000000
y_ceil = 4000000

y_lines = [[[0, x_ceil]] for i in range(y_ceil + 1)]


def line_intersection(x11, x12, x21, x22):
    lines = []
    if x21 < x11:
        lines.append([x21, min(x22, x11 - 1)])
    if x12 < x22:
        lines.append([max(x12 + 1, x21), x22])
    return lines


def handle_intersection(x, y, manh):
    global x_ceil, y_ceil, y_lines
    for y_i in range(max(y - manh, 0), min(y + manh, y_ceil) + 1):
        x_width = get_x_width(manh, y, y_i)
        current_lines = y_lines[y_i]
        if current_lines:
            new_segments = []
            for line in current_lines:
                new_segments += line_intersection(max(0, x - x_width), min(x + x_width, x_ceil), *line)
            y_lines[y_i] = new_segments


for sensor in sensors:
    s_x, s_y, b_x, b_y = [int(i) for i in findall(cord_regex, sensor)]
    if b_y == y_row:
        x_beacons[f"{b_x}:{b_y}"] = '#'
    manh = get_manhattan(s_x, s_y, b_x, b_y)
    handle_intersection(s_x, s_y, manh)


for index, line in enumerate(y_lines):
    if line != []:
        print(line[0][0] * 4000000 + index)
