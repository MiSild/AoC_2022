from common_aoc import read_file_n
from operator import add, mul
from typing import List
from copy import deepcopy
from math import lcm

monkey_input = read_file_n(11)
op_to_fn = {
    '+': add,
    '*': mul
}


class Monkey:
    def __init__(self, items: List[int], operator, operand, divider, true_monkey: int, false_monkey: int):
        self.items = items
        self.operator = op_to_fn[operator]
        self.operand = operand
        self.divider = int(divider)
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.inspections = 0
        self.monkeys = []

    def set_monkeys(self, monkeys):
        self.monkeys = monkeys

    def receive_item(self, worry: int):
        self.items.append(worry)

    def inspect_item(self, worry: int):
        if self.operand == 'old':
            return self.operator(worry, worry)
        else:
            return self.operator(worry, int(self.operand))

    def take_turn(self, reducer=None):
        while len(self.items) > 0:
            item_worry = self.items.pop(0)
            if reducer is None:
                item_worry = int(self.inspect_item(item_worry) / 3)
            else:
                item_worry = self.inspect_item(item_worry) % reducer
            if item_worry % self.divider == 0:
                self.monkeys[self.true_monkey].receive_item(item_worry)
            else:
                self.monkeys[self.false_monkey].receive_item(item_worry)
            self.inspections += 1


class MonkeyBusiness:
    def __init__(self, monkeys: List["Monkey"]):
        self.monkeys = monkeys

    def do_business(self, times: int, reducer=None):
        for i in range(times):
            for monkey in self.monkeys:
                monkey.take_turn(reducer)
        return self.get_monkey_business_level()

    def get_monkey_business_level(self):
        inspections = []
        for monkey in self.monkeys:
            inspections.append(monkey.inspections)

        inspections.sort()
        return inspections[-1] * inspections[-2]


monkeys = []
divisors = []
for i in range(int((len(monkey_input) + 1) / 7)):
    items = [int(monkey_input[i*7 + 1][0].split(": ")[1])] + [int(x) for x in monkey_input[i*7 + 1][1:]]
    operator, operand = monkey_input[i*7 + 2][0].split("old ")[1].split(" ")
    divider = int(monkey_input[i*7 + 3][0].split(" ")[-1])
    divisors.append(divider)
    true_monkey = int(monkey_input[i*7 + 4][0].split(" ")[-1])
    false_monkey = int(monkey_input[i*7 + 5][0].split(" ")[-1])
    new_monkey = Monkey(items, operator, operand, divider, true_monkey, false_monkey)
    monkeys.append(new_monkey)

for monkey in monkeys:
    monkey.set_monkeys(monkeys)
business_p1 = MonkeyBusiness(monkeys)
business_p2 = deepcopy(business_p1)
reducer = lcm(*divisors)

print(business_p1.do_business(20))
print(business_p2.do_business(10000, reducer))

