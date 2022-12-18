from common_aoc import read_file_n


def abs_diff(a, b):
    return abs(a - b)


def cubes_touching(cube1, cube2):
    return sum(map(abs_diff, cube1, cube2)) == 1


def get_blockable_cubes(cube):
    x, y, z = cube
    return [[x, y, z + 1], [x, y, z - 1], [x + 1, y, z], [x, y - 1, z], [x - 1, y, z], [x, y + 1, z]]


cubes = read_file_n(18)
cubes = [[int(x) for x in cube] for cube in cubes]
sides = len(cubes) * 6
for i, cube in enumerate(cubes):
    for j in range(i, len(cubes)):
        if cubes_touching(cube, cubes[j]):
            sides -= 2

print(sides)

sides = len(cubes) * 6
trapped = {}
for i, cube in enumerate(cubes):
    blocked = get_blockable_cubes(cube)
    for block in blocked:
        if [*block] not in cubes:
            trapped[f"{block[0]}:{block[1]}:{block[2]}"] = trapped.get(f"{block[0]}:{block[1]}:{block[2]}", 0) + 1
    for j in range(i, len(cubes)):
        if cubes_touching(cube, cubes[j]):
            sides -= 2


def follow_air_pocket(cube, air_cubes):
    global cubes
    cube_str = f"{cube[0]}:{cube[1]}:{cube[2]}"
    touchings = [x for x in get_blockable_cubes(cube) if f"{x[0]}:{x[1]}:{x[2]}" in trapped]
    if 6 - trapped[cube_str] == len(touchings):
        for t in [x for x in touchings if f"{x[0]}:{x[1]}:{x[2]}" not in air_cubes]:
            air_cubes.add(f"{t[0]}:{t[1]}:{t[2]}")
            new_air = follow_air_pocket(t, air_cubes)
            if new_air == []:
                return []
            else:
                for i in new_air:
                    air_cubes.add(i)
        return air_cubes
    else:
        return []


checked = []
for blocked_cube, blocked_sides in trapped.items():
    if blocked_cube not in checked:
        cube = [int(x) for x in blocked_cube.split(":")]
        air_cubes = set([blocked_cube])
        air_cubes = follow_air_pocket(cube, air_cubes)
        if len(air_cubes) > 0:
            print(air_cubes)
        for air_cube in air_cubes:
            sides -= trapped[air_cube]
            checked.append(air_cube)
print(sides)
