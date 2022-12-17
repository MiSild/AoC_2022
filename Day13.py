from common_aoc import read_file_n
from functools import cmp_to_key

packets = read_file_n(13, "inputs", True)
pair = []
packets_clean = []
for i, row in enumerate(packets):
    if row == '':
        packets_clean.append(pair)
        pair = []
        continue
    pair.append(eval(row))
packets_clean.append(pair)
packets = packets_clean


def compare_pair(left, right):
    if type(left) == int and type(right) == int:
        if left < right:
            return -1
        elif left > right:
            return 1
        else:
            return 0
    elif type(left) == list and type(right) == list:
        for i in zip(left, right):
            comparison = compare_pair(i[0], i[1])
            if comparison == -1:
                return -1
            elif comparison == 1:
                return 1
        if len(left) < len(right):
            return -1
        elif len(left) == len(right):
            return 0
        else:
            return 1
    else:
        if type(left) == int:
            return compare_pair([left], right)
        else:
            return compare_pair(left, [right])


summa = 0
for i, pair in enumerate(packets):
    if compare_pair(pair[0], pair[1]) == -1:
        summa += i + 1

print(summa)

packets = [i for sublist in packets for i in sublist]
packets.append([[2]])
packets.append([[6]])

sorted_packets = sorted(packets, key=cmp_to_key(compare_pair))
decoder_key = 1
for i, packet in enumerate(sorted_packets):
    if packet in [[[2]], [[6]]]:
        decoder_key = decoder_key * (i + 1)
print(decoder_key)
