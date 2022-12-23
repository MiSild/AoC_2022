from common_aoc import read_file_n

input = read_file_n(22, 'inputs', True)
grid = []
direction_raw = input[-1]
directions = []
step = ''
walk_path = {'x': {}, 'y': {}}
x_offsets = {}
y_offsets = {}
r = {
    'N': 'E',
    'E': 'S',
    'S': 'W',
    'W': 'N'
}

l = {
    'N': 'W',
    'E': 'N',
    'S': 'E',
    'W': 'S'
}

turns = {'R': r, 'L': l}

for letter in direction_raw:
    if letter in "RL":
        directions.append(int(step))
        directions.append(letter)
        step = ''
    else:
        step += letter
directions.append(int(step))

for i, row in enumerate(input):
    if row == '':
        break
    else:
        for j, letter in enumerate(row):
            if letter != ' ':
                walk_path['x'][j] = walk_path['x'].get(j, '') + letter
                if i not in x_offsets:
                    x_offsets[i] = j
                if j not in y_offsets:
                    y_offsets[j] = i
        walk_path['y'][i] = row.strip()


def walk_on_path(start_index, no_steps, path, step):
    path_l = len(path)
    for i in range(no_steps):
        next_i = (start_index + step) % path_l
        if path[next_i] == '#':
            return start_index
        else:
            start_index = next_i
    return next_i


facing = 'E'
y = 0
x = x_offsets[0]
for instruction in directions:
    if type(instruction) == int:
        if facing in "WE":
            path = walk_path['y'][y]
            step = -1 if facing == 'W' else 1
            x = walk_on_path(x - x_offsets[y], instruction, path, step) + x_offsets[y]
        else:
            path = walk_path['x'][x]
            step = 1 if facing == 'S' else -1
            y = walk_on_path(y - y_offsets[x], instruction, path, step) + y_offsets[x]
    else:
        facing = turns[instruction][facing]
facing_to_value = {
    'N': 3, 'E': 0, 'S': 1, 'W': 2
}
print(1000 * (y + 1) + 4 * (x + 1) + facing_to_value[facing])

swap_axis = {
    'x': 'y',
    'y': 'x'
}

switch_90 = {
    'N': {True: 'E', False: 'W'},
    'S': {True: 'W', False: 'E'},
    'E': {True: 'N', False: 'S'},
    'W': {True: 'E', False: 'N'}
}

switch = {
    'N': {True: 'S', False: 'N'},
    'S': {True: 'N', False: 'S'},
    'E': {True: 'W', False: 'E'},
    'W': {True: 'E', False: 'W'}
}


class Face:
    def __init__(self, index, x_start, x_index, y_start, y_index):
        global walk_path
        self.index = index
        self.x_2d_offset = x_start
        self.y_2d_offset = y_start
        self.rows = {'x': [walk_path['x'][i][y_index:y_index + 50] for i in range(x_start, x_start + 50)],
                     'y': [walk_path['y'][i][x_index:x_index + 50] for i in range(y_start, y_start + 50)]}
        self.faces = None
        self.row_orientations = {'x': [], 'y': []}  # ala [[1, False, False], [2, False, False], [4, True, True], [5, True, True]

    def get_row(self, xy, index, flag_reverse_order=False, flag_reverse_index=False):
        row = self.rows[xy]
        row = row[49 - index] if flag_reverse_index else row[index]
        return row[::-1] if flag_reverse_order else row

    def get_cube_row(self, xy, index):
        cube_row = ''
        face_indexes = []
        for face_index, flag_reverse_order, flag_reverse_index, sub_xy in self.row_orientations[xy]:
            cube_row += self.faces[face_index - 1].get_row(sub_xy, index, flag_reverse_order, flag_reverse_index)
            face_indexes.append(face_index)
        return cube_row, index, face_indexes

    def walk_on_cube(self, x_index, y_index, orientation, no_steps):
        flag_reverse = False
        if orientation in 'NW':
            flag_reverse = True
        xy = 'x' if orientation in 'NS' else 'y'
        stat_index, mov_index = [x_index, y_index] if xy == 'x' else [y_index, x_index]
        cube_row, index, face_indexes = self.get_cube_row(xy, stat_index)
        if orientation in 'NW':
            cube_row = cube_row[::-1]
            index = 199 - index
            face_indexes = face_indexes[::-1]
        new_index = walk_on_path(index, no_steps, cube_row, 1)
        face_index = face_indexes[new_index // 50]
        new_index = new_index % 50
        _, flag_ro, flag_ri, target_axis = [row_orientation for row_orientation in self.row_orientations[xy] if row_orientation[0] == face_index][0]
        new_state = {}
        new_state[target_axis] = 49 - stat_index if flag_ri else stat_index
        new_state[swap_axis[target_axis]] = new_index if flag_reverse + flag_ro % 2 == 0 else 49 - new_index
        new_orientation = switch[orientation][flag_ro] if target_axis == xy else switch_90[orientation][flag_ro]
        return new_state, face_index, new_orientation


# 5 - row_orientations['x'] = [[5, False, False, 'x'], [6, False, False, 'x'], [2, False, False, 'x'], [3, True, False, 'y']]
# - 1 2
# - 3 -
# 5 4 -
# 6 - -

faces = [Face(1, 50, 0, 0, 0)
         , Face(2, 100, 50, 0, 0)
         , Face(3, 50, 0, 50, 50)
         , Face(4, 50, 50, 100, 100)
         , Face(5, 0, 0, 100, 0)
         , Face(6, 0, 0, 150, 50)]
for face in faces:
    face.faces = faces

faces[0].row_orientations = {'x': [[1, False, False, 'x'], [3, False, False, 'x'], [4, False, False, 'x'], [6, True, False, 'y']],
                             'y': [[1, False, False, 'y'], [2, False, False, 'y'],
                                   [4, True, True, 'y'], [5, True, True, 'y']]}
faces[1].row_orientations = {'x': [[2, False, False, 'x'], [3, True, False, 'y'], [5, False, False, 'x'], [6, False, False, 'x']],
                             'y': [[2, False, False, 'y'], [4, True, True, 'y'],
                                   [5, True, True, 'y'], [1, False, False, 'x']]}
faces[2].row_orientations = {'x': [[3, False, False, 'x'], [4, False, False, 'x'], [6, True, False, 'y'], [1, False, False, 'x']],
                             'y': [[3, False, False, 'y'], [2, True, False, 'x'],
                                   [6, True, False, 'x'], [5, True, False, 'x']]}
faces[3].row_orientations = {'x': [[4, False, False, 'x'], [6, True, False, 'y'], [1, False, False, 'x'], [3, False, False, 'x']],
                             'y': [[4, False, False, 'y'], [2, True, True, 'y'], [1, True, True, 'y'],
                                   [5, False, False, 'y']]}
faces[4].row_orientations = {'x': [[5, False, False, 'x'], [6, False, False, 'x'], [2, False, False, 'x'], [3, True, False, 'y']],
                             'y': [[5, False, False, 'y'], [4, False, False, 'y'],
                                   [2, True, True, 'y'], [1, True, True, 'y']]}
faces[5].row_orientations = {'x': [[6, False, False, 'x'], [2, False, False, 'x'], [3, True, False, 'y'], [5, False, False, 'x']],
                             'y': [[6, False, False, 'y'], [4, True, False, 'x'],
                                   [3, True, False, 'x'], [1, True, False, 'x']]}
facing = 'E'
x, y = [0, 0]
face = 1
#         return new_state, face_index, new_orientation
for instruction in directions:
    if type(instruction) == int:
        new_state, face, facing = faces[face - 1].walk_on_cube(x, y, facing, instruction)
        x = new_state['x']
        y = new_state['y']
    else:
        facing = turns[instruction][facing]

