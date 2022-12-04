from common_aoc import read_file_n


def is_complete_overlap(first, second):
    if first[0] <= second[0] and first[1] >= second[1]:
        return True
    elif first[0] >= second[0] and first[1] <= second[1]:
        return True
    else:
        return False


def is_partial_overlap(first, second):
    if second[0] <= first[0] <= second[1]:
        return True
    elif first[0] <= second[0] <= first[1]:
        return True
    else:
        return False


assignments = read_file_n(4)
complete_count = 0
partial_count = 0
for assignment_pair in assignments:
    first, second = assignment_pair
    first = [int(x) for x in first.split('-')]
    second = [int(x) for x in second.split('-')]
    if is_complete_overlap(first, second):
        complete_count += 1
    if is_partial_overlap(first, second):
        partial_count += 1

print(f"There is a complete overlap for {complete_count} assignments")
print(f"There is a partial overlap for {partial_count} assignments")

