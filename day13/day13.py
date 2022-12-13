

def parse_input(input_path):
    """Return a list of pairs of packets."""
    pairs = []
    with open(input_path) as file_obj:
        pair = []
        for line in file_obj:
            if line.strip():
                pair.append(eval(line.strip()))
            else:
                pairs.append(pair)
                pair = []
    return pairs


def day13a(input_path):
    """Return the sum of indices of pairs that are in the correct order."""
    pairs = parse_input(input_path)
    index_sum = 0
    for ind, pair in enumerate(pairs):
        if Packet(pair[0]) < Packet(pair[1]):
            index_sum += (ind + 1)
    return index_sum


class Packet:
    """Capture the convoluted Day 13 comparison logic and overlaod the comparison operators."""

    def __init__(self, val):
        self.val = val

    def __lt__(self, other):
        return self.compare_lists(other) == 1

    def __eq__(self, other):
        return self.compare_lists(other) == 0

    def __gt__(self, other):
        return self.compare_lists(other) == -1

    def check_pair(self, other):
        """Return 1 if self < other, 0 if they are equal, and -1 if self > other (unknown types)."""
        if isinstance(self.val, int) and isinstance(other.val, int):
            if self.val < other.val:
                return 1
            if self.val > other.val:
                return -1
            return 0
        elif isinstance(self.val, list) and isinstance(other.val, list):
            return self.compare_lists(other)
        elif isinstance(self.val, int):
            self.val = [self.val]
            return self.compare_lists(other)
        elif isinstance(other.val, int):
            other.val = [other.val]
            return self.compare_lists(other)
        else:
            raise ValueError(f"Unexpected types {type(self.val)} and {type(other.val)}")

    def compare_lists(self, other):
        """Return 1 if self < other, 0 if they are equal, and -1 if self > other (both lists)."""
        for ind in range(len(other.val)):
            if ind == len(self.val):  # self.val is shorter than other.val
                return 1
            result = Packet(self.val[ind]).check_pair(Packet(other.val[ind]))
            if result != 0:
                return result
            continue
        if len(self.val) == len(other.val):
            return 0
        return -1  # self.val is longer than other.val


def test13a():
    assert Packet([1, 1, 3, 1, 1]) < Packet([1, 1, 5, 1, 1])
    assert Packet([[1], [2, 3, 4]]) < Packet([[1], 4])
    assert 13 == day13a('test_input.txt')


def parse_input_b(input_path):
    """Return a list of all packets (not paired)."""
    packets = []
    with open(input_path) as file_obj:
        for line in file_obj:
            if line.strip():
                packets.append(eval(line.strip()))
    return packets


def day13b(input_path):
    """Return the product of the indices of the first and second divider packets after sorting."""
    packets = parse_input_b(input_path)
    first = [[2]]
    second = [[6]]
    packets += [first, second]
    packets = [Packet(p) for p in packets]
    packets = sorted(packets)

    first_ind = 0
    second_ind = 0
    for ind, packet in enumerate(packets):
        if packet.val == first:
            first_ind = ind + 1
            continue
        if packet.val == second:
            second_ind = ind + 1
            break
    return first_ind * second_ind


def test13b():
    assert 140 == day13b('test_input.txt')


if __name__ == '__main__':
    test13a()
    print('Day 13a:', day13a('day13_input.txt'))
    test13b()
    print('Day 13b:', day13b('day13_input.txt'))
