from common_aoc import read_file_n

numbers = [[int(x[0]), i] for i, x in enumerate(read_file_n(20))]
boundary = len(numbers) - 1


def mix_round(number_list):
    for index, pair in enumerate(number_list):
        step, location = pair
        new_location = (location + step) % boundary
        numbers[index] = [step, new_location]
        for bump_index, bump_pair in enumerate(numbers):
            if bump_index == index:
                continue
            bump_number, bump_location = bump_pair
            if location < bump_location <= new_location:
                bump_step = -1
            elif new_location <= bump_location < location:
                bump_step = 1
            else:
                bump_step = 0
            numbers[bump_index] = [bump_pair[0], bump_location + bump_step]


def get_number_order(number_list, flag_zeroth=False):
    ordered = [0 for i in range(boundary + 1)]
    zeroth = 0
    for check in number_list:
        ordered[check[1]] = check[0]
        if check[0] == 0:
            zeroth = check[1]
    if flag_zeroth:
        return ordered, zeroth
    else:
        return ordered


mix_round(numbers)
ordered, zeroth = get_number_order(numbers, True)
print(ordered[(zeroth + 1000) % (boundary + 1)] + ordered[(zeroth + 2000) % (boundary + 1)] + ordered[(zeroth + 3000) % (boundary + 1)])


# Part 2
decryption_key = 811589153
numbers = [[int(x[0]) * decryption_key, i] for i, x in enumerate(read_file_n(20))]
for i in range(10):
    mix_round(numbers)
ordered, zeroth = get_number_order(numbers, True)
print(ordered[(zeroth + 1000) % (boundary + 1)] + ordered[(zeroth + 2000) % (boundary + 1)] + ordered[(zeroth + 3000) % (boundary + 1)])