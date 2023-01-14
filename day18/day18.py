import numpy as np


def parse_input(input_path):
    """Return a list of lists of cube coordinates."""
    cube_list = []
    with open(input_path) as file_obj:
        for line in file_obj:
            cube_list.append([int(num) for num in line.split(',')])
    return cube_list


def day18a(input_path):
    """Return the estimated surface area of the flying lava blobs."""
    cube_list = parse_input(input_path)
    cube_coords = np.array(cube_list)
    # max possible area is 6 per cube
    area = 6 * len(cube_list)

    def count_adjacent(array):
        deltas = np.diff(array, axis=0)
        return np.all(deltas == np.array([1, 0, 0]), axis=1).sum()

    # subtract 2 from max possible area for each adjacent cube
    # need to check for adjacent cubes in 3 dimensions, so reorder columns and sort them three ways
    inds = np.lexsort(cube_coords.T)
    cube_coords = cube_coords[inds]
    area -= 2 * count_adjacent(cube_coords)

    cube_coords = np.roll(cube_coords, 1, axis=1)
    inds = np.lexsort(cube_coords.T)
    cube_coords = cube_coords[inds]
    area -= 2 * count_adjacent(cube_coords)

    cube_coords = np.roll(cube_coords, 1, axis=1)
    inds = np.lexsort(cube_coords.T)
    cube_coords = cube_coords[inds]
    area -= 2 * count_adjacent(cube_coords)

    return area


def test18a():
    assert 64 == day18a('test_input.txt')


def day18b(input_path):
    pass


def test18b():
    assert 58 == day18b('test_input.txt')


if __name__ == '__main__':
    test18a()
    print('Day 18a:', day18a('day18_input.txt'))
    # test18b()
    # print('Day 18b:', day18b('day18_input.txt'))
