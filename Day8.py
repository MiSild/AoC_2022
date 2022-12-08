from common_aoc import read_file_n

trees = read_file_n(8)

tree_rows = [[int(x) for x in row[0]] for row in trees]
tree_cols = [*map(list, zip(*tree_rows))]
length = len(tree_rows)
width = len(tree_rows[0])
heights = {}

visible_count = 0
best_score = 0


def is_visible(i, height, tree_row):
    return max(tree_row[:i] + [-1]) < height or height > max(tree_row[i + 1:] + [-1])


def count_visibility(i, height, tree_row):
    counts = 1
    tree_chunks = [tree_row[i + 1:], tree_row[:i][::-1]]
    for chunk in tree_chunks:
        count = 0
        for tree in chunk:
            if tree < height:
                count += 1
            else:
                count += 1
                break
        counts = counts * count
    return counts


for y, row in enumerate(tree_rows):
    for x, height in enumerate(row):
        visible_count += int(is_visible(x, height, row) or is_visible(y, height, tree_cols[x]))
        score = count_visibility(x, height, row) * count_visibility(y, height, tree_cols[x])


# Discarded solution path


def cord_to_key(x: int, y: int) -> str:
    return f"{x}:{y}"


def update_down(x, y, height, height_map):
    for y_i in range(y, length):
        key = cord_to_key(x, y_i)
        height_map[key] = max(height_map.get(key, 0), height)


def update_up(x, y, height, height_map):
    for y_i in range(y, -1, -1):
        key = cord_to_key(x, y_i)
        height_map[key] = max(height_map.get(key, 0), height)


def update_left(x, y, height, height_map):
    for x_i in range(x, -1, -1):
        key = cord_to_key(x_i, y)
        height_map[key] = max(height_map.get(key, 0), height)


def update_right(x, y, height, height_map):
    for x_i in range(x, width):
        key = cord_to_key(x_i, y)
        height_map[key] = max(height_map.get(key, 0), height)

