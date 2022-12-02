

def day02a(input_path):
    """Return my total score from following the strategy guide, I think."""
    with open(input_path) as file_obj:
        total = 0
        for line in file_obj:
            score = 0
            moves = [ord(move) for move in line.strip().split()]
            moves[0] -= 64  # A --> 1, B --> 2, C --> 3
            moves[1] -= 87  # X --> 1, Y --> 2, Z --> 3
            # A means opponent will play rock, Y paper, Z scissors
            # X means I should play rock, Y paper, Z scissors
            score += moves[1]  # shape points
            outcome_points = 0
            if moves[0] == moves[1]:
                outcome_points = 3  # draw
            elif (moves[0] == moves[1] - 1) or (moves[0] == moves[1] + 2):
                outcome_points = 6  # win
            score += outcome_points
            total += score
    return total


def test02a():
    assert 15 == day02a('test_input.txt')


def day02b(input_path):
    """Return my total score from following the *actual* strategy guide."""
    with open(input_path) as file_obj:
        total = 0
        for line in file_obj:
            score = 0
            moves = [ord(move) for move in line.strip().split()]
            moves[0] -= 64  # A --> 1, B --> 2, C --> 3
            moves[1] -= 87  # X --> 1, Y --> 2, Z --> 3
            # A means opponent will play rock, Y paper, Z scissors
            # X means I should lose, Y means I should draw, Z means I should win
            if moves[1] == 1:  # lose
                outcome_points = 0
                shape_points = moves[0] - 1
                if shape_points < 1:
                    shape_points += 3
            elif moves[1] == 2:  # draw
                outcome_points = 3
                shape_points = moves[0]
            else:  # win
                outcome_points = 6
                shape_points = moves[0] + 1
                if shape_points > 3:
                    shape_points -= 3
            score += shape_points
            score += outcome_points
            total += score
    return total


def test02b():
    assert 12 == day02b('test_input.txt')


if __name__ == '__main__':
    test02a()
    print('Day 02a:', day02a('day02_input.txt'))
    test02b()
    print('Day 02b:', day02b('day02_input.txt'))
