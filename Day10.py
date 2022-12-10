from common_aoc import read_file_n

operations = [operation[0].split(" ") for operation in read_file_n(10)]

register = 1
cycle = 1
signal_strength = 0
lit_pixel = '⬜'
dark_pixel = '⬛'
pixels = ''


def next_cycle(add=0):
    global cycle, signal_strength, register, pixels
    if abs(register - len(pixels) % 40) < 2:
        pixels = pixels + lit_pixel
    else:
        pixels = pixels + dark_pixel
    cycle += 1
    register += add
    if cycle == 20 or (cycle - 20) % 40 == 0:
        print(f"Cycle {cycle} with register {register} for signal strength {cycle * register}")
        signal_strength += cycle * register


for operation in operations:
    if operation[0] == 'noop':
        next_cycle()
    else:
        next_cycle()
        next_cycle(int(operation[1]))

for i in range(6):
    print(pixels[i*40:(i+1)*40])



