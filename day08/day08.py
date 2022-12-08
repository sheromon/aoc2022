import numpy as np


def parse_input(input_path):
    with open(input_path) as file_obj:
        lines = [list(line.strip()) for line in file_obj]
    return np.array(lines).astype(int)


def day08a(input_file):
    array = parse_input(input_file)

    # start by assuming no trees are visible
    visible = np.zeros_like(array)

    # but we know that all trees on the border are visible
    visible[0, :] = 1
    visible[-1, :] = 1
    visible[:, 0] = 1
    visible[:, -1] = 1

    # check visibility of interior trees coming from each of the four directions
    visible |= check_visibility_top_to_bottom(array)
    visible |= check_visibility_top_to_bottom(array[::-1, :])[::-1, :]
    visible |= check_visibility_top_to_bottom(array.T).T
    visible |= check_visibility_top_to_bottom(array.T[::-1, :])[::-1, :].T

    return np.sum(np.sum(visible))


def check_visibility_top_to_bottom(array):
    """For each column of trees (skipping borders), check each tree's visibility from the top of the row going down."""
    visible = np.zeros_like(array)
    for icol in range(1, array.shape[1]):
        max_val = array[0, icol]
        for irow in range(1, array.shape[0]):
            val = array[irow, icol]
            if val > max_val:
                max_val = val
                visible[irow, icol] = 1
    return visible


def test08a():
    assert 21 == day08a('test_input.txt')


def day08b(input_file):
    """Return the maximum possible scenic score for any tree in the given grid of tree heights."""
    array = parse_input(input_file)
    n_row, n_col = array.shape

    max_score = 0
    for irow in range(1, n_row - 1):
        for icol in range(1, n_col - 1):
            score = calc_score(array, irow, icol)
            if score > max_score:
                max_score = score
    return max_score


def calc_distance(row):
    """For a line of sight (a row of trees), calculate the number of trees that can be seen from the first tree."""
    house_height = row[0]
    visible = 0
    for height in row[1:]:
        visible += 1
        if height >= house_height:
            break
    return visible


def calc_score(array, irow, icol):
    """Calculate a scenic score for a specific tree in the grid of trees."""
    score = 1
    # looking up
    score *= calc_distance(array[irow::-1, icol])
    # looking left
    score *= calc_distance(array[irow, icol::-1])
    # looking down
    score *= calc_distance(array[irow:, icol])
    # looking right
    score *= calc_distance(array[irow, icol:])
    return score


def test08b():
    array = parse_input('test_input.txt')

    score = calc_score(array, irow=1, icol=2)
    assert score == 4

    score = calc_score(array, irow=3, icol=2)
    assert score == 8

    # I added my own test case to catch something that was missing in the provided test cases
    score = calc_score(array, irow=2, icol=1)
    assert score == 6

    assert 8 == day08b('test_input.txt')


if __name__ == '__main__':
    test08a()
    print('Day 08a:', day08a('day08_input.txt'))
    test08b()
    print('Day 08b:', day08b('day08_input.txt'))
