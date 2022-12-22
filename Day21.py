from common_aoc import read_file_n
from operator import add, mul, sub, truediv, eq
from sympy.solvers import solve
from sympy import Symbol, Eq

op_to_fn = {
    '+': add,
    '*': mul,
    '/': truediv,
    '-': sub,
    '==': Eq
}

monkeys = read_file_n(21, "inputs", True)
monkeys = [[x.split(": ")[0], x.split(": ")[1].split(" ")] for x in monkeys]

shouts = {}

for name, yell in monkeys:
    if len(yell) == 1:
        shouts[name] = int(yell[0])
    else:
        shouts[name] = yell


def get_equation(monkey_name):
    global shouts
    shout = shouts[monkey_name]
    if type(shout) == int or type(shout) == Symbol:
        return shout
    else:
        monkey_1, operator, monkey_2 = shout
        return_value = op_to_fn[operator](get_equation(monkey_1), get_equation(monkey_2))
        return return_value


print(get_equation("root"))

shouts['root'][1] = '=='
x = Symbol('x')
shouts['humn'] = x

print(solve(get_equation('root'), x))
