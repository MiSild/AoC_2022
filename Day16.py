from common_aoc import read_file_n
import heapq
from scipy.sparse.csgraph import floyd_warshall

valves = read_file_n(16, 'inputs', True)
valves = {valve.split("Valve ")[1][:2]: [int(valve.split("rate=")[-1].split(";")[0]), valve.split("valves ")[-1].split(', ')] for valve in valves}

# AADDCCBBAAIIJJIIAADDEEFFGGHHGGFFEEDDCC, 1651, DDBBJJHHEECC
minutes = 30
heap = []

rated_valves = set()
valve_to_index = {}
index_to_valve = {}
index = 0
for key, valve in valves.items():
    valve_to_index[key] = index
    index_to_valve[index] = key
    index += 1
    if valve[0] > 0:
        rated_valves.add(key)

# Calculate the shortest path to valves with rates from any other node
distances = [[999999999 for x in range(len(valves))] for y in range(len(valves))]
for key, valve in valves.items():
    for connection in valve[1]:
        distances[valve_to_index[key]][valve_to_index[connection]] = 1

dist_matrix = floyd_warshall(distances, True, False, False)


def upper_bound_pressure_potential(time_left, unopened_valves):
    global valves
    pressure_potential = 0
    for unopened in unopened_valves:
        pressure_potential += time_left * valves[unopened][0]
    return pressure_potential


# -Pressure-to-be-released, current position, opened valves, time_left, opening order
heapq.heappush(heap, (0, "AA", set(), 30, ""))
pressure = 0
while len(heap) > 0:
    pwr, current_position, opened_valves, minutes_left, opening_order = heapq.heappop(heap)
    if pwr < pressure:
        pressure = pwr
    if pwr - upper_bound_pressure_potential(minutes_left, rated_valves - opened_valves) > pressure:
        continue
    for unopened_rated_valve in rated_valves - opened_valves:
        travel_time = dist_matrix[valve_to_index[current_position]][valve_to_index[unopened_rated_valve]]
        post_opening_time = minutes_left - travel_time - 1
        if post_opening_time > 0:
            destination_rate, _ = valves[unopened_rated_valve]
            new_open_valves = set(opened_valves)
            new_open_valves.add(unopened_rated_valve)
            heapq.heappush(heap, (pwr - (destination_rate * post_opening_time), unopened_rated_valve, new_open_valves, post_opening_time, opening_order + unopened_rated_valve))

print(pressure * -1)


# Part 2
def get_who_moves_where(des, des_2, person_des, dest, dest_2, opening_orders):
    if person_des is None:
        return [[dest, dest_2], [des, des_2], [opening_orders[0]+dest, opening_orders[1]+dest_2]]
    else:
        return [[dest_2, dest], [des_2, des], [opening_orders[1]+dest_2, opening_orders[0]+dest]]


def push_faster_move_to_heap(destination_valve, rate, travel_time, destination_valve_2, rate_2, travel_time_2, des_2, new_open_valves, heap, person_des, minutes_left, opening_orders):
    # Given where both parties are, new destinations, travel times and rates. Teleport the parties further in time the smaller segment of time
    if des_2 > 0:  # This means that only one entity gets a new destination
        time_step = min(travel_time, des_2)
        new_positions, new_des, new_opening_orders = get_who_moves_where(travel_time - time_step, des_2 - time_step, person_des, destination_valve, destination_valve_2, opening_orders)
        heapq.heappush(heap, (pwr - (rate * (minutes_left - travel_time)), new_positions, new_open_valves, minutes_left - time_step, new_des, new_opening_orders))
    else:
        time_step = min(travel_time, travel_time_2)
        if minutes_left - max(travel_time, travel_time_2) - 1 > 0:
            new_positions, new_des, new_opening_orders = get_who_moves_where(travel_time - time_step, travel_time_2 - time_step, person_des, destination_valve, destination_valve_2, opening_orders)
            heapq.heappush(heap, (pwr - (rate * (minutes_left - travel_time)) - (rate_2 * (minutes_left - travel_time_2)), new_positions, new_open_valves, minutes_left - time_step, new_des, new_opening_orders))


heapq.heappush(heap, (0, ["AA", "AA"], set(), 26, [0, 0], ["", ""]))
pressure = 0
while len(heap) > 0:
    pwr, current_positions, opened_valves, minutes_left, time_to_destinations, opening_orders = heapq.heappop(heap)
    if pwr < pressure:
        pressure = pwr
        # print(f"Pressure: {pwr}, times: {time_to_destinations}, final_pos: {current_positions}, opened: {opened_valves}, opening_order:{opening_orders}")
    if pwr - upper_bound_pressure_potential(minutes_left, rated_valves - opened_valves) * 2 > pressure:  # IDK how much better an elephant makes it but 50 times seems enough to have it hold true
        continue
    person_pos, elephant_pos = current_positions
    person_des, elephant_des = time_to_destinations
    for destination_valve in rated_valves - opened_valves:
        pos = person_pos if person_des == 0 else elephant_pos
        rate, _ = valves[destination_valve]
        travel_time = dist_matrix[valve_to_index[pos]][valve_to_index[destination_valve]]
        if time_to_destinations == [0, 0]:
            pos_2 = elephant_pos if person_des == 0 else person_pos
            des_2 = elephant_des if person_des == 0 else person_des
            for destination_valve_2 in rated_valves - opened_valves:
                new_open_valves = set(opened_valves)
                new_open_valves.add(destination_valve)
                travel_time_2 = dist_matrix[valve_to_index[pos_2]][valve_to_index[destination_valve_2]]
                rate_2, _ = valves[destination_valve_2]
                if destination_valve_2 == destination_valve and len(rated_valves - opened_valves) != 1:
                    continue
                if len(rated_valves - opened_valves) == 1:
                    fastest_time = travel_time if travel_time < travel_time_2 else travel_time_2
                    if minutes_left - fastest_time - 1 > 0:
                        heapq.heappush(heap, (pwr - (rate * (minutes_left - fastest_time - 1)), [destination_valve, elephant_pos], new_open_valves, minutes_left - fastest_time - 1, [0, 0], [opening_orders[0] + destination_valve, opening_orders[1]]))
                else:
                    new_open_valves.add(destination_valve_2)
                    push_faster_move_to_heap(destination_valve, rate, travel_time + 1, destination_valve_2, rate_2, travel_time_2 + 1, des_2, new_open_valves, heap, person_des, minutes_left, opening_orders)
        else:
            pos_2 = person_pos if person_des != 0 else elephant_pos
            des_2 = person_des if person_des != 0 else elephant_des
            new_open_valves = set(opened_valves)
            new_open_valves.add(destination_valve)
            push_faster_move_to_heap(destination_valve, rate, travel_time + 1, pos_2, 0, 0, des_2, new_open_valves, heap, person_des, minutes_left, opening_orders)

print(-1 * pressure)

