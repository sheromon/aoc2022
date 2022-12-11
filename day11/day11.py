import operator


def day11a(input_path):
    """Return the level of monkey business after 20 rounds of monkeys throwing items around."""
    monkey_list = parse_input(input_path)
    for _ in range(20):
        for monkey in monkey_list:
            take_turn(monkey, monkey_list)
    counts = sorted([monkey.count for monkey in monkey_list])
    return counts[-1] * counts[-2]


def test11a():
    assert 10605 == day11a('test_input.txt')


def day11b(input_path):
    """Return the level of monkey business after 10000 rounds of monkeys throwing items around.

    Note that there is no worry reduction this time.
    """
    monkey_list = parse_input(input_path)
    convert_ints(monkey_list)
    for _ in range(10000):
        for monkey in monkey_list:
            take_turn(monkey, monkey_list, worry_reduction=False)
    counts = sorted([monkey.count for monkey in monkey_list])
    return counts[-1] * counts[-2]


def convert_ints(monkey_list):
    """Convert worry level integer values to a different format for the purposes of solving this problem."""
    divisors = sorted([m.test['multiple'] for m in monkey_list])
    for monkey in monkey_list:
        monkey.item_list = [MonkeyCentricInt(val, divisors) for val in monkey.item_list]


def test11b():
    assert 2713310158 == day11b('test_input.txt')


def parse_input(input_path):
    """Parse the input file and return a list of monkeys in order of monkey index, starting from 0."""
    with open(input_path) as file_obj:
        lines = [line.strip() for line in file_obj]

    lines.reverse()  # reverse so we can pop off each line from the end
    line = lines.pop()

    # monkey ids seem to be integers from 0 to n, so we can easily get any monkey by indexing a list
    monkeys = []

    while lines:

        while lines and not line:
            line = lines.pop()

        assert line.startswith('Monkey')
        remainder = line[len('Monkey'):]
        monkey_id = int(remainder.split(':')[0].strip())
        assert monkey_id == len(monkeys)  # verify that monkey ids match expectations
        line = lines.pop()

        assert line.startswith('Starting items:')
        remainder = line[len('Starting items:'):].strip()
        item_list = [int(item) for item in remainder.split(',')]
        line = lines.pop()

        assert line.startswith('Operation:')
        remainder = line[len('Operation:'):].strip()
        assert remainder.startswith('new = ')
        remainder = remainder.split('=')[-1].strip()
        if remainder == 'old * old':
            op = pow
            val = 2
        elif remainder.startswith('old *'):
            op = operator.mul
            val = int(remainder[len('old *'):])
        elif remainder.startswith('old +'):
            op = operator.add
            val = int(remainder[len('old +'):])
        else:
            raise RuntimeError(f"Unrecognized operation '{remainder}'")
        operation = {'op': op, 'val': val}
        line = lines.pop()

        assert line.startswith('Test:')
        remainder = line[len('Test:'):].strip()
        multiple = int(remainder.split()[-1])
        line = lines.pop()

        assert line.startswith('If true:')
        remainder = line[len('If true:'):].strip()
        true_monkey = int(remainder.split()[-1])
        line = lines.pop()

        assert line.startswith('If false:')
        remainder = line[len('If false:'):].strip()
        false_monkey = int(remainder.split()[-1])
        if lines:
            line = lines.pop()

        test = {
            'multiple': multiple,
            'true_monkey': true_monkey,
            'false_monkey': false_monkey,
        }

        new_monkey = Monkey(
            monkey_id=monkey_id, operation=operation, item_list=item_list, test=test,
        )
        monkeys.append(new_monkey)

    return monkeys


class Monkey:
    """Store the relevant attributes of each monkey."""

    def __init__(self, monkey_id, operation, item_list, test):
        self.id = monkey_id
        self.operation = operation
        self.item_list = item_list
        self.test = test
        self.count = 0

    def __str__(self):
        output = [
            f'ID: {self.id}',
            f'  operation: {self.operation}',
            f'  item_list: {str(self.item_list)}',
            f'  test: {self.test}',
        ]
        return '\n'.join(output) + '\n'


def take_turn(monkey, monkey_list, worry_reduction=True):
    """For a given monkey, iterate through all that monkey's items and pass them appropriately."""
    for item in monkey.item_list:
        monkey.count += 1
        # update item worry level due to monkey inspection
        item = monkey.operation['op'](item, monkey.operation['val'])
        # if worry_reduction is happening, reduce worry level
        if worry_reduction:
            item = item // 3
        # monkey tests worry level
        if item % monkey.test['multiple'] == 0:
            recipient = monkey.test['true_monkey']
        else:
            recipient = monkey.test['false_monkey']
        # monkey passes item to recipient
        monkey_list[recipient].item_list.append(item)
    monkey.item_list = []


class MonkeyCentricInt:
    """Store information about a worry value that is relevant to the monkey situation."""

    def __init__(self, val, divisors):
        self.remainder_map = {d: val % d for d in divisors}

    def __repr__(self):
        return str(self.remainder_map)

    def __mul__(self, other):
        for d, remainder in self.remainder_map.items():
            self.remainder_map[d] = (remainder * other) % d
        return self

    def __add__(self, other):
        for d, remainder in self.remainder_map.items():
            self.remainder_map[d] = (remainder + other) % d
        return self

    def __pow__(self, power):
        for d, remainder in self.remainder_map.items():
            self.remainder_map[d] = pow(remainder, power, mod=d)
        return self

    def __mod__(self, other):
        return self.remainder_map[other]


if __name__ == '__main__':
    test11a()
    print('Day 11a:', day11a('day11_input.txt'))
    test11b()
    print('Day 11b:', day11b('day11_input.txt'))
