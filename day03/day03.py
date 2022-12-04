

def parse_input(input_path):
    with open(input_path) as file_obj:
        lines = [line.strip() for line in file_obj]
    return lines


def day03a(input_path):
    """Return the sum of the priorities of the duplicate items in each rucksack."""
    lines = parse_input(input_path)
    total = 0
    for line in lines:
        first, second = line[:len(line)//2], line[len(line)//2:]
        common_set = set(first) & set(second)
        assert len(common_set) == 1  # common set should have only one element
        common = ord(common_set.pop())
        if common < 97:  # A to Z --> 27 to 52
            common -= 38
        else:  # a to z --> 1 to 26
            common -= 96
        total += common
    return total


def test03a():
    assert 157 == day03a('test_input.txt')


def day03b(input_path):
    """Return the sum of the priorities of the items common to each group of three elves."""
    lines = parse_input(input_path)
    total = 0
    for ind in range(0, len(lines), 3):
        common_set = set(lines[ind]) & set(lines[ind+1]) & set(lines[ind+2])
        assert len(common_set) == 1  # common set should have only one element
        common = ord(common_set.pop())
        if common < 97:  # A to Z --> 27 to 52
            common -= 38
        else:  # a to z --> 1 to 26
            common -= 96
        total += common
    return total


def test03b():
    assert 70 == day03b('test_input.txt')


if __name__ == '__main__':
    test03a()
    print('Day 03a:', day03a('day03_input.txt'))
    test03b()
    print('Day 03b:', day03b('day03_input.txt'))
