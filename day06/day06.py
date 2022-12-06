

def find_marker(input_file, num_unique):
    """Return the minimum number of characters that must be processed to find the marker."""
    if input_file.endswith('.txt'):
        line = open(input_file).read().strip()
    else:
        line = input_file

    for ichar in range(len(line) - num_unique):
        chars = line[ichar:ichar + num_unique]
        if len(set(chars)) == num_unique:
            return ichar + num_unique


def day06a(input_file):
    return find_marker(input_file, num_unique=4)


def test06a():
    assert 7 == day06a('mjqjpqmgbljsphdztnvjfqwrcgsmlb')


def day06b(input_file):
    return find_marker(input_file, num_unique=14)


def test06b():
    assert 19 == day06b('mjqjpqmgbljsphdztnvjfqwrcgsmlb')


if __name__ == '__main__':
    test06a()
    print('Day 06a:', day06a('day06_input.txt'))
    test06b()
    print('Day 06b:', day06b('day06_input.txt'))
