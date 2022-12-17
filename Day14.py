from common_aoc import read_file_n
from copy import deepcopy

rock_lines = read_file_n(14, "inputs", True)
rock_lines = [[[int(i) for i in pair.split(',')] for pair in row.split(' -> ')] for row in rock_lines]
y_floor = 0


def get_rocks_from_line(start_x, start_y, end_x, end_y):
    if start_x <= end_x:
        x_inc = 1
    else:
        x_inc = -1
    if start_y <= end_y:
        y_inc = 1
    else:
        y_inc = -1

    rocks = []
    for x in range(start_x, end_x + x_inc, x_inc):
        for y in range(start_y, end_y + y_inc, y_inc):
            rocks.append([x, y])
    return rocks


def get_sand_movements(x, y, stuff):
    global y_floor
    movements = [[x, y + 1], [x - 1, y + 1], [x + 1, y + 1]]
    return [movement for movement in movements if stuff.get(f"{movement[0]}:{movement[1]}", "") != "#" and movement[1] < y_floor]


def infinite_falling_break(sand_y, stuff):
    global y_floor
    return sand_y >= y_floor - 1


def blocked_up_break(sand_y, stuff):
    return stuff.get("500:0", "") == "#"


def simulate_sand(stuff, break_function):
    sand_x, sand_y = [500, 0]
    sand_blocks = 1
    while True:
        movements = get_sand_movements(sand_x, sand_y, stuff)
        if break_function(sand_y, stuff):
            return sand_blocks - 1
        elif len(movements) == 0:
            stuff[f"{sand_x}:{sand_y}"] = "#"
            sand_blocks += 1
            sand_x, sand_y = [500, 0]
        else:
            sand_x, sand_y = movements[0]


things = {}

for lines in rock_lines:
    for i in range(len(lines) - 1):
        rocks = get_rocks_from_line(lines[i][0], lines[i][1], lines[i+1][0], lines[i+1][1])
        for rock in rocks:
            things[f"{rock[0]}:{rock[1]}"] = "#"
            if rock[1] > y_floor - 2:
                y_floor = rock[1] + 2


things_p2 = deepcopy(things)
print(simulate_sand(things, infinite_falling_break))
print(simulate_sand(things_p2, blocked_up_break))


