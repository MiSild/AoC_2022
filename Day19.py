from common_aoc import read_file_n
from re import findall
import heapq
from copy import deepcopy
from random import shuffle


class Blueprint:
    def __init__(self, index, ore_cost, clay_cost, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian):
        self.index = int(index)
        self.ore_cost = int(ore_cost)
        self.clay_cost = int(clay_cost)
        self.obsidian_ore_cost = int(obsidian_ore)
        self.obsidian_clay_cost = int(obsidian_clay)
        self.geode_ore_cost = int(geode_ore)
        self.geode_obsidian_cost = int(geode_obsidian)


class State:
    def __init__(self, blueprint: "Blueprint", minutes):
        self.ore = 0
        self.ore_robots = 1
        self.clay = 0
        self.clay_robots = 0
        self.obsidian_robots = 0
        self.geode_robots = 0
        self.geodes = 0
        self.obsidian = 0
        self.minutes = minutes
        self.blueprint = blueprint
        self.history = ""
        self.max_ore = max(self.blueprint.ore_cost, self.blueprint.geode_ore_cost, self.blueprint.obsidian_ore_cost, self.blueprint.clay_cost)
        self.max_clay = self.blueprint.obsidian_clay_cost
        self.max_obsidian = self.blueprint.geode_obsidian_cost

    def __lt__(self, other):
        if self.geodes == other.geodes:
            return self.geodes > other.geodes
        else:
            return self.minutes > other.minutes

    def __le__(self, other):
        if self.geodes == other.geodes:
            return self.geodes >= other.geodes
        else:
            return self.minutes >= other.minutes

    def tick_time(self, minutes: int):
        if minutes == 0:
            return
        self.minutes -= minutes
        self.clay += minutes * self.clay_robots
        self.ore += minutes * self.ore_robots
        self.obsidian += minutes * self.obsidian_robots
        self.geodes += minutes * self.geode_robots

    def create_ore_robot(self):
        if self.ore_robots >= self.max_ore:
            return False
        while self.ore < self.blueprint.ore_cost:
            self.tick_time(1)
            if self.minutes == 0:
                return False
        self.tick_time(1)
        self.ore_robots += 1
        self.ore -= self.blueprint.ore_cost
        self.history += f"{self.minutes}:Ore:"

    def create_clay_robot(self):
        if self.clay_robots >= self.max_clay:
            return False
        while self.ore < self.blueprint.clay_cost:
            self.tick_time(1)
            if self.minutes == 0:
                return False
        self.tick_time(1)
        self.clay_robots += 1
        self.ore -= self.blueprint.clay_cost
        self.history += f"{self.minutes}:Clay:"

    def create_obsidian_robot(self):
        if self.obsidian_robots >= self.max_obsidian or self.clay_robots == 0:
            return False
        while self.ore < self.blueprint.obsidian_ore_cost or self.clay < self.blueprint.obsidian_clay_cost:
            self.tick_time(1)
            if self.minutes == 0:
                return False
        self.tick_time(1)
        self.obsidian_robots += 1
        self.clay -= self.blueprint.obsidian_clay_cost
        self.ore -= self.blueprint.obsidian_ore_cost
        self.history += f"{self.minutes}:Obsidian:"

    def create_geode_robot(self):
        if self.obsidian < self.blueprint.geode_obsidian_cost and self.obsidian_robots == 0:
            return False
        while self.ore < self.blueprint.geode_ore_cost or self.obsidian < self.blueprint.geode_obsidian_cost:
            self.tick_time(1)
            if self.minutes == 0:
                return False
        self.tick_time(1)
        self.geode_robots += 1
        self.obsidian -= self.blueprint.geode_obsidian_cost
        self.ore -= self.blueprint.geode_ore_cost
        self.history += f"{self.minutes}:Geode:"

    def do_action(self, action):
        return self.action_options[action]()

    @property
    def action_options(self):
        return [self.create_ore_robot, self.create_clay_robot, self.create_obsidian_robot, self.create_geode_robot]

    def max_resources_gathered(self, rate):
        resources = 0
        for i in range(1, self.minutes):
            resources += (rate + 0.5 * i) * (self.minutes - i)
        return resources

    def upper_potential_bound(self):
        geodes = self.geode_robots * self.minutes + self.geodes
        return geodes + self.minutes * (self.minutes - 1) / 2

    def geode_score(self):
        return int(self.geodes + self.geode_robots * self.minutes)


def get_best_state(blueprint: "Blueprint", minutes: int):
    heap = []
    heapq.heappush(heap, (0, State(blueprint, minutes)))
    best_geodes = 0
    best_state = None
    while len(heap) > 0:
        score, state = heapq.heappop(heap)
        if score < best_geodes:
            best_geodes = score
            best_state = state
        if state.minutes <= 0 or -state.upper_potential_bound() > best_geodes:
            continue
        indexes = [0, 1, 2, 3]
        shuffle(indexes)
        for new, i in enumerate(indexes):
            if new != 3:
                new_state = deepcopy(state)
            else:
                new_state = state
            if new_state.do_action(i) is not False:
                heapq.heappush(heap, (min(-new_state.geode_score(), -new_state.obsidian_robots * 0.1), new_state))
    return best_state


blueprints = read_file_n(19)
blueprints = [Blueprint(*findall('\d+', blueprint[0])) for blueprint in blueprints]
blueprint_scores = [get_best_state(x, 24) for x in blueprints]
print(sum([x.blueprint.index * x.geode_score() for x in blueprint_scores]))

part_2 = [get_best_state(x, 32) for x in blueprints[:3]]
product = 1
for x in part_2:
    product = product * x.geode_score()
print(product)
