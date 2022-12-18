from common_aoc import read_file_n


def abs_diff(a, b):
    return abs(a - b)


def cubes_touching(cube1, cube2):
    return sum(map(abs_diff, cube1, cube2)) == 1


def get_neighbouring_cubes(cube):
    x, y, z = cube
    neighbours = [[x, y, z + 1], [x, y, z - 1], [x + 1, y, z], [x, y - 1, z], [x - 1, y, z], [x, y + 1, z]]
    return [tuple(x) for x in neighbours if all(-1 <= i <= 22 for i in x)]


cubes = read_file_n('18')
cubes = [tuple([int(x) for x in cube]) for cube in cubes]
sides = len(cubes) * 6
sides_outside = 0
trapped = {}
for i, cube in enumerate(cubes):
    blocked = get_neighbouring_cubes(cube)
    for j in range(i, len(cubes)):
        if cubes_touching(cube, cubes[j]):
            sides -= 2
print(sides)

start_cube = (-1, -1, -1)
visited = set()
heap = [start_cube]
sides_seen = {}
while len(heap) > 0:
    current_cube = heap.pop()
    visited.add(current_cube)
    for neighbour in get_neighbouring_cubes(current_cube):
        if neighbour in cubes:
            sides_seen[neighbour] = sides_seen.get(neighbour, 0) + 1
            sides_outside += 1
        elif neighbour not in visited and neighbour not in heap:
            heap.append(neighbour)
print(sides_outside)
