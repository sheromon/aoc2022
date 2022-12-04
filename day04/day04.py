

def parse_input(input_path):
    with open(input_path) as file_obj:
        lines = [line.strip() for line in file_obj]
    return lines


def day04a(input_path):
    """Return the number of pairs with fully overlapping assignments."""
    lines = parse_input(input_path)
    total = 0
    for line in lines:
        first, second = line.split(',')
        first = [int(val) for val in first.split('-')]
        second = [int(val) for val in second.split('-')]
        # get the deltas between the mins and maxs of the two sections
        deltas = [second[ind] - first[ind] for ind in range(2)]
        if deltas[0] * deltas[1] <= 0:
            total += 1
    return total


def test04a():
    assert 2 == day04a('test_input.txt')


def day04b(input_path):
    """Return the number of pairs with any overlap in assignments."""
    lines = parse_input(input_path)
    total = 0
    for line in lines:
        first, second = line.split(',')
        first = [int(val) for val in first.split('-')]
        second = [int(val) for val in second.split('-')]
        if (first[0] <= second[1]) and (second[0] <= first[1]):
            total += 1
        elif (second[0] <= first[1]) and (first[0] <= second[1]):
            total += 1
    return total


def test04b():
    assert 4 == day04b('test_input.txt')


if __name__ == '__main__':
    test04a()
    print('Day 04a:', day04a('day04_input.txt'))
    test04b()
    print('Day 04b:', day04b('day04_input.txt'))
