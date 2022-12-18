from common_aoc import read_file_n


def abs_diff(a, b):
    return abs(a - b)


def cubes_touching(cube1, cube2):
    return sum(map(abs_diff, cube1, cube2)) == 1


def get_neighbouring_cubes(cube):
    x, y, z = cube
    return [[x, y, z + 1], [x, y, z - 1], [x + 1, y, z], [x, y - 1, z], [x - 1, y, z], [x, y + 1, z]]


cubes = read_file_n('18_2', 'example')
cubes = [[int(x) for x in cube] for cube in cubes]
sides = len(cubes) * 6
trapped = {}
for i, cube in enumerate(cubes):
    blocked = get_neighbouring_cubes(cube)
    for block in blocked:
        if [*block] not in cubes:
            trapped[f"{block[0]}:{block[1]}:{block[2]}"] = trapped.get(f"{block[0]}:{block[1]}:{block[2]}", 0) + 1
    for j in range(i, len(cubes)):
        if cubes_touching(cube, cubes[j]):
            sides -= 2
print(sides)


def follow_air_pocket(cube, airpocket_cubes):
    global trapped
    cube_str = f"{cube[0]}:{cube[1]}:{cube[2]}"
    neighbours = [x for x in get_neighbouring_cubes(cube) if f"{x[0]}:{x[1]}:{x[2]}" in trapped]  # Blocked side neighbours
    if 6 - trapped[cube_str] == len(neighbours):  # Every side that is not blocked by lava needs to have an air pocket with blocked sides
        for n in [x for x in neighbours if f"{x[0]}:{x[1]}:{x[2]}" not in airpocket_cubes]:  # Pocket cubes we have not checked
            airpocket_cubes.add(f"{n[0]}:{n[1]}:{n[2]}")
            new_air = follow_air_pocket(n, airpocket_cubes)
            if new_air == set():
                return set()
    else:
        return set()


checked = []
for blocked_cube in trapped.keys():
    if blocked_cube not in checked:
        cube = [int(x) for x in blocked_cube.split(":")]
        airpocket_cubes = {blocked_cube}
        air = follow_air_pocket(cube, airpocket_cubes)
        if air == set():
            continue
        if len(airpocket_cubes) > 0:
            print(airpocket_cubes)
        for air_cube in airpocket_cubes:
            sides -= trapped[air_cube]
            checked.append(air_cube)
print(sides)
