from common_aoc import read_file_n

signal = read_file_n(6)[0]

for i in range(4, len(signal)):
    if len(set(signal[i-4:i])) == 4:
        print(i)
        break

for i in range(14, len(signal)):
    if len(set(signal[i-14:i])) == 14:
        print(i)
        break
