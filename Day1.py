import common_aoc as C

lines = C.read_file_n(1)
elf_calories = []
elf_lines = []
for line in lines:
    if line != ['']:
        elf_lines.append(line[0])
    else:
        elf_calories.append(elf_lines)
        elf_lines = []

elf_placeholder = {}
for elf in elf_calories:
    elf_placeholder[sum([int(i) for i in elf])] = [int(i) for i in elf]
elf_calories = elf_placeholder

calory_sum = 0
calories = list(elf_calories.keys())
for i in range(3):
    most_calories = max(calories)
    calory_sum += most_calories
    calories.remove(most_calories)
    print(most_calories)

print(calory_sum)
