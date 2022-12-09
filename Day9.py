from common_aoc import read_file_n
from operator import add

steps = read_file_n(9)
steps = [step[0].split(" ") for step in steps]

straight_movements = {
    'R': [1, 0],
    'U': [0, 1],
    'L': [-1, 0],
    'D': [0, -1]
}
diagonal_movements = {
    'UR': [1, 1],
    'UL': [-1, 1],
    'DL': [-1, -1],
    'DR': [1, -1]
}


def are_touching(h_x, h_y, t_x, t_y):
    return (h_x == t_x and abs(h_y - t_y) < 2) or (h_y == t_y and abs(h_x - t_x) < 2) or (
            h_x == t_x + 1 and h_y == t_y - 1) or (h_x == t_x - 1 and h_y == t_y - 1) or (
            h_x == t_x - 1 and h_y == t_y + 1) or (h_x == t_x + 1 and h_y == t_y + 1)


def make_move(cords, move):
    return list(map(add, cords, move))


def tail_to_head(head, tail):
    if head[0] == tail[0] or head[1] == tail[1]:
        moves = straight_movements.values()
    else:
        moves = diagonal_movements.values()
    for move in moves:
        new_pos = make_move(tail, move)
        if are_touching(*head, *new_pos):
            return new_pos


def cord_to_key(x, y):
    return f"{x}:{y}"


head = [0, 0]
tail = [0, 0]
seen_cords = {"0:0": 1}

for step in steps:
    for i in range(int(step[1])):
        head = make_move(head, straight_movements[step[0]])
        if not are_touching(*head, *tail):
            tail = tail_to_head(head, tail)
            seen_cords[cord_to_key(*tail)] = 1

print(len(seen_cords.keys()))

knots = [[0, 0] for i in range(10)]
seen_cords = {"0:0": 1}
for step in steps:
    for i in range(int(step[1])):
        knots[0] = make_move(knots[0], straight_movements[step[0]])
        for j in range(9):
            if not are_touching(*knots[j], *knots[j + 1]):
                knots[j + 1] = tail_to_head(knots[j], knots[j + 1])
                if j == 8:
                    seen_cords[cord_to_key(*knots[j + 1])] = 1

print(len(seen_cords.keys()))

