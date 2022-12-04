from common_aoc import read_file_n

strategy_guide = read_file_n(2)
strategy_guide = [x[0].split(' ') for x in strategy_guide]
shape_to_points = {
    'rock': 1,
    'paper': 2,
    'scissors': 3
}

letter_to_shape = {
    'A': 'rock',
    'X': 'rock',
    'B': 'paper',
    'Y': 'paper',
    'C': 'scissors',
    'Z': 'scissors'
}

shape_to_loser = {
    'rock': 'scissors',
    'paper': 'rock',
    'scissors': 'paper'
}

shape_to_winner = {
    'rock': 'paper',
    'paper': 'scissors',
    'scissors': 'rock'
}

def calculate_showoff_points(opponent, self):
    if self == opponent:
        return 3
    elif shape_to_winner[opponent] == self:
        return 6
    else:
        return 0


def calculate_pair_score(pair):
    opponent, self = pair
    opponent = letter_to_shape[opponent]
    self = letter_to_shape[self]
    points = shape_to_points[self]
    return points + calculate_showoff_points(opponent, self)


total_points = 0
for match in strategy_guide:
    total_points += calculate_pair_score(match)
print(f"The total score for part 1 is : {total_points}")

result_to_points = {
    'X': 0,
    'Y': 3,
    'Z': 6
}


def get_shape_for_result(opponent, result):
    opponent = letter_to_shape[opponent]
    if result == 'Y':
        return opponent
    elif result == 'X':
        return shape_to_loser[opponent]
    else:
        return shape_to_winner[opponent]


def calculate_pair_score_strategy(pair):
    opponent, result = pair
    points = result_to_points[result]
    self_shape = get_shape_for_result(opponent, result)
    return points + shape_to_points[self_shape]


total_points = 0
for match in strategy_guide:
    total_points += calculate_pair_score_strategy(match)
print(f"The total score for part 2 is : {total_points}")


