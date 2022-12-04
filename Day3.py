from common_aoc import read_file_n

rucksacks = read_file_n(3)
rucksacks = [x[0] for x in rucksacks]


def get_priority(letter):
    letter = ord(letter)
    if letter > 96:
        return letter - 96
    else:
        return letter - 38


def get_compartments_from_rucksack(rucksack):
    split = int(len(rucksack) / 2)
    return rucksack[:split], rucksack[split:]


def get_common_character_in_compartments(first, second):
    for letter in first:
        if letter in second:
            return letter

points = 0
for rucksack in rucksacks:
    common = get_common_character_in_compartments(*get_compartments_from_rucksack(rucksack))
    points += get_priority(common)

print(f"The sum of the priority: {points}")


def get_common_in_group(group):
    first, second, third = [set(x) for x in group]
    common = first.intersection(second).intersection(third)
    return common.pop()


elf_groups = []
for index, rucksack in enumerate(rucksacks):
    if index % 3 == 0:
        if index != 0:
            elf_groups.append(group)
        group = [rucksack]
    else:
        group.append(rucksack)
elf_groups.append(group)

total_points = 0
for group in elf_groups:
    total_points += get_priority(get_common_in_group(group))

print(f"The total priority of the badges is: {total_points}")
