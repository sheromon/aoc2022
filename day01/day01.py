

def day01a(input_path):
    """Return the maximum total number of calories carried by a single elf."""
    max_elf = 0
    with open(input_path) as file_obj:
        this_elf = 0
        for line in file_obj:
            val = line.strip()
            if val:
                this_elf += int(val)
            else:
                if this_elf > max_elf:
                    max_elf = this_elf
                this_elf = 0
    if this_elf > max_elf:
        max_elf = this_elf
    return max_elf


def test01a():
    assert 24000 == day01a('test_input.txt')


def day01b(input_path):
    """Return the sum of the top three maximum total calories carried by individual elves."""
    max_elves = [0, 0, 0]
    with open(input_path) as file_obj:
        this_elf = 0
        for line in file_obj:
            val = line.strip()
            if val:
                this_elf += int(val)
            else:
                if this_elf > max_elves[0]:
                    max_elves[0] = this_elf
                    max_elves = sorted(max_elves)
                this_elf = 0
    if this_elf > max_elves[0]:
        max_elves[0] = this_elf
        max_elves = sorted(max_elves)
    return sum(max_elves)


def test01b():
    assert 45000 == day01b('test_input.txt')


if __name__ == '__main__':
    test01a()
    print('Day 01a:', day01a('day01_input.txt'))
    test01b()
    print('Day 01b:', day01b('day01_input.txt'))
