import numpy as np


DIRECTION_TO_DELTA = {
    'R': np.array([0, 1]),
    'L': np.array([0, -1]),
    'U': np.array([-1, 0]),
    'D': np.array([1, 0]),
}


def parse_input(input_path):
    moves = []
    with open(input_path) as file_obj:
        for line in file_obj:
            tokens = line.strip().split()
            moves.append([tokens[0], int(tokens[1])])
    return moves


def calc_visits(moves, num_tails=1, size=500):
    """For a given set of moves, calculate the number of unique positions that the rope tail visits.

    Args:
        moves: list of moves, where each move is a sequence (direction, num_steps); direction is a letter in 'U', 'D',
            'L', 'R', and num_steps is an integer
        num_tails: optional int; number of tails in rope; defaults to 1
        size: optional int; size of grid of all possible positions; yes, I could have tried to intelligently calculate
            an appropriate size, but this worked

    Returns:
        int, total number of unique positions visited by the last tail
    """
    grid = np.zeros([size, size], int)
    head = size // 2 * np.ones(2, int)
    tails = size // 2 * np.ones([num_tails, 2], int)
    for direction, num in moves:
        head_delta = DIRECTION_TO_DELTA[direction]
        for _ in range(num):
            head += head_delta
            prev = head
            for itail in range(len(tails)):
                gap = prev - tails[itail]
                if np.any(np.abs(gap) > 1):
                    tail_delta = np.minimum(np.abs(gap), np.array([1, 1])) * np.sign(gap)
                    tails[itail] += tail_delta
                prev = tails[itail]
            grid[tuple(tails[-1])] = 1
    return np.sum(np.sum(grid))


def day09a(input_file):
    moves = parse_input(input_file)
    return calc_visits(moves)


def test09a():
    assert 13 == day09a('test_input.txt')


def day09b(input_file):
    moves = parse_input(input_file)
    return calc_visits(moves, num_tails=9)


def test09b():
    assert 1 == day09b('test_input.txt')


if __name__ == '__main__':
    test09a()
    print('Day 09a:', day09a('day09_input.txt'))
    test09b()
    print('Day 09b:', day09b('day09_input.txt'))
