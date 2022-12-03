

def day02a(input_path):
    """Return my total score from following the strategy guide, I think."""
    with open(input_path) as file_obj:
        total = 0
        for line in file_obj:
            score = 0
            moves = [ord(move) for move in line.strip().split()]
            yours, mine = moves
            yours -= 64  # A --> 1, B --> 2, C --> 3
            mine -= 87  # X --> 1, Y --> 2, Z --> 3
            # A means opponent will play rock, Y paper, Z scissors
            # X means I should play rock, Y paper, Z scissors
            score += mine  # shape points
            offset = (yours - mine) % 3
            if offset == 0:
                outcome_points = 3  # draw
            elif offset == 1:
                outcome_points = 0  # lose
            else:
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
            moves = [ord(move) for move in line.strip().split()]
            yours, outcome = moves
            yours -= 64  # A --> 1, B --> 2, C --> 3
            outcome -= 87  # X --> 1, Y --> 2, Z --> 3
            # A means opponent will play rock, Y paper, Z scissors
            # X means I should lose, Y means I should draw, Z means I should win
            if outcome == 1:  # lose
                outcome_points = 0
                shape_points = yours - 1
                if shape_points < 1:
                    shape_points += 3
            elif outcome == 2:  # draw
                outcome_points = 3
                shape_points = yours
            else:  # win
                outcome_points = 6
                shape_points = yours + 1
                if shape_points > 3:
                    shape_points -= 3
            score = shape_points + outcome_points
            total += score
    return total


def test02b():
    assert 12 == day02b('test_input.txt')


if __name__ == '__main__':
    test02a()
    print('Day 02a:', day02a('day02_input.txt'))
    test02b()
    print('Day 02b:', day02b('day02_input.txt'))
