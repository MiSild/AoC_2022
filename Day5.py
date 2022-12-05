from common_aoc import read_file_n
from copy import deepcopy

lines = read_file_n(5)

crate_mode = True
crates = {}
instructions = []
for line in lines:
    line = line[0]
    if line == '':
        crate_mode = False
    elif crate_mode:
        for i in range(1, 35, 4):
            if line[i] != ' ':
                existing = crates.get(int(i / 4) + 1, [])
                existing.insert(0, line[i])
                crates[int(i / 4) + 1] = existing
    else:
        instruction = line.split(' ')
        instructions.append([instruction[1], instruction[3], instruction[5]])


def move_boxes(start, destination, amount, crate_map, reorder: bool):
    to_move = crate_map[start][-amount:]
    del crate_map[start][-amount:]
    if reorder:
        to_move = to_move[::-1]
    crate_map[destination] = crate_map[destination] + to_move


part_one_crates = deepcopy(crates)
part_two_crates = deepcopy(crates)
for instruction in instructions:
    amount, start, destination = [int(x) for x in instruction]
    move_boxes(start, destination, amount, part_one_crates, True)
    move_boxes(start, destination, amount, part_two_crates, False)


result_one = ''
result_two = ''
for i in range(1, 10):
    result_one += part_one_crates[i][-1]
    result_two += part_two_crates[i][-1]

print(result_one)
print(result_two)
