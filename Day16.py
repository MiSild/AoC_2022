from common_aoc import read_file_n
import heapq

valves = read_file_n(16, 'example', True)
valves = {valve.split("Valve ")[1][:2]: [int(valve.split("rate=")[-1].split(";")[0]), valve.split("valves ")[-1].split(', ')] for valve in valves}

# What describes a path is the valves traveled + pressure that will be released without further action (pwr) + minutes left
# The same sorted path is better if it has the same pressure but more minutes left or same minutes but more pwr
# (-pwr, path, minutes)
# AADDCCBBAAIIJJIIAADDEEFFGGHHGGFFEEDDCC
minutes = 30
heap = []

heapq.heappush(heap, (0, "AA", 30))
valve_set = set(valves.keys())
pressure = 0
while len(heap) > 0:
    pwr, path, minutes_left = heapq.heappop(heap)
    if pwr < pressure:
        pressure = pwr
    if set(path) == valve_set:
        continue
    _, connections = valves[path[-2:]]
    for connection in connections:
        rate, _ = valves[connection]
        new_combo = None
        if (rate == 0 or connection in path) and minutes_left > 3:  # Time to move here + somewhere else and open valve and let some pressure out
            new_combo = (pwr, path + connection, minutes_left - 1)
        elif minutes_left > 2:
            new_combo = (pwr - rate * (minutes_left - 2), path + connection, minutes_left - 2)
        if new_combo:
            sorted_path = sorted((path + connection))

            to_delete = []
            should_push = False
            never_found = True
            for i, el in enumerate(heap):
                if sorted_path == sorted(el[1]):
                    never_found = False
                    if new_combo[0] == el[0] and new_combo[2] > el[2]:
                        to_delete.append(i)
                        should_push = True
                        continue
                    elif new_combo[2] == el[2] and new_combo[0] < el[0]:
                        to_delete.append(i)
                        should_push = True
                        continue
            for index in sorted(to_delete, reverse=True):
                del heap[index]
            if never_found or should_push:
                heapq.heappush(heap, new_combo)







