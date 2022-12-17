from common_aoc import read_file_n
import heapq

maze = read_file_n(12)
maze = [[x for x in row[0]] for row in maze]

max_x = len(maze[0])
max_y = len(maze)
start_x = 0
start_y = 0
for y in range(len(maze)):
    if maze[y][start_x] == 'S':
        start_y = y
        break


def get_neighbour_indexes(x, y, max_x, max_y):
    neighbours = [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]
    return [n for n in neighbours if 0 <= n[0] < max_x and 0 <= n[1] < max_y]


def get_neighbours(x, y, max_x, max_y, maze):
    n_i = get_neighbour_indexes(x, y, max_x, max_y)
    current_h = maze[y][x]
    if current_h == 'S':
        current_h = 'a'
    return [n for n in n_i if (ord(maze[n[1]][n[0]]) - ord(current_h) <= 1 and maze[n[1]][n[0]] != 'E')
            or (maze[n[1]][n[0]] == 'E' and ord(current_h) >= 121)]


def key_from_indexes(x, y):
    return f"{x}:{y}"


def find_path_from_start_to_end(start_x, start_y, max_x, max_y, maze):
    score_map = {key_from_indexes(start_x, start_y): 0}
    heap = []
    heapq.heappush(heap, (0, start_x, start_y))

    while len(heap) > 0:
        current = heapq.heappop(heap)
        if maze[current[2]][current[1]] == 'E':
            return current[0]
        neighbours = get_neighbours(current[1], current[2], max_x, max_y, maze)
        for n in neighbours:
            if key_from_indexes(n[0], n[1]) not in score_map:
                score_map[key_from_indexes(n[0], n[1])] = current[0] + 1
                heapq.heappush(heap, (current[0] + 1, n[0], n[1]))

    return 10000000000000000


print(find_path_from_start_to_end(start_x, start_y, max_x, max_y, maze))
# Part 2
path_lengths = []
for y_i in range(len(maze)):
    for x_i in range(len(maze[0])):
        if maze[y_i][x_i] == 'a':
            path_lengths.append(find_path_from_start_to_end(x_i, y_i, max_x, max_y, maze))

path_lengths.sort()
print(path_lengths[0])








