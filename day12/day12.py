import queue

import numpy as np


def parse_input(input_path):
    lines = []
    with open(input_path) as file_obj:
        for line in file_obj:
            lines.append([ord(c) for c in line.strip()])
    return np.array(lines)


def day12a(input_path):
    """Return the minimum number of steps needed to go from the start to the end of the height map."""
    array = parse_input(input_path)
    hmap = HeightMap(array)
    hmap.explore()
    return hmap.min_from_end[hmap.start_coords[0]]


def test12a():
    assert 31 == day12a('test_input.txt')


def day12b(input_path):
    """Return the minimum number of steps needed to go from any possible start to the end of the height map."""
    array = parse_input(input_path)
    hmap = HeightMap(array, any_start=True)
    hmap.explore()
    return min(hmap.min_from_end[coords] for coords in hmap.start_coords)


def test12b():
    assert 29 == day12b('test_input.txt')


class HeightMap:
    """Represents the height map and minimum number of steps needed to reach the ending square."""

    def __init__(self, array, any_start=False):
        array = np.pad(array, ((1, 1), (1, 1)), 'constant', constant_values=0)
        # convert the cell that marks the start to have a value equivalent to 'a'
        inds = array == ord('S')
        assert np.sum(inds.flatten()) == 1
        array[inds] = ord('a')
        start_coords = [tuple(np.concatenate(np.where(inds)))]
        # convert the cell that marks the end to have a value equivalent to 'z'
        inds = array == ord('E')
        assert np.sum(inds.flatten()) == 1
        array[inds] = ord('z')
        end_coords = np.concatenate(np.where(inds))

        self.heights = array  # array of height values
        self.start_coords = start_coords  # list of tuples of x-y coordinates of starting square
        if any_start:
            self.update_start_coords()
        self.end_coords = end_coords  # x-y coordinates of ending square
        self.coords = end_coords  # x-y coordinates of current square
        self.completed = np.zeros(len(self.start_coords), bool)  # boolean indicating whether each start was reached

        # keep track of the minimum number of steps needed to reach the ending square
        self.min_from_end = array.size * np.ones_like(array).astype(int)
        self.min_from_end[tuple(self.end_coords)] = 0  # the ending square has value 0 by definition

        # keep track of paths that still need to be explored
        self.unexplored_paths = queue.SimpleQueue()

    def update_start_coords(self):
        """Update start coords to include any square at elevation 'a' (part 2 only)."""
        self.start_coords = list(zip(*np.stack(np.where(self.heights == ord('a'))).tolist()))

    def assess_steps(self):
        """For adjacent squares that can reach the current square, update min steps from end.

        If any adjacent squares can reach the current square and do so using the minimum number of steps observed so
        far, then return those steps as valid steps to explore further.
        """
        deltas = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
        valid_steps = []
        for delta in deltas:
            next_coords = self.coords + delta
            height_delta = self.heights[tuple(self.coords)] - self.heights[tuple(next_coords)]
            if height_delta > 1:
                continue  # cannot reach current square from this one
            current_steps = self.min_from_end[tuple(self.coords)]
            next_steps = current_steps + 1
            # only update the min steps from end and mark this step as a valid path if the number of
            # steps is smaller than the previous min number of steps; don't want to waste time exploring
            # paths that we know are not the shortest
            if next_steps < self.min_from_end[tuple(next_coords)]:
                self.min_from_end[tuple(next_coords)] = next_steps
                # if we reached a starting point, mark it as having been reached
                if tuple(next_coords) in self.start_coords:
                    ind = self.start_coords.index(tuple(next_coords))
                    self.completed[ind] = True
                valid_steps.append(delta)
        return valid_steps

    def explore(self):
        """Fill out the array with minimum number of steps to reach the end square."""
        while (not np.all(self.completed)) or (not self.unexplored_paths.empty()):
            valid_steps = self.assess_steps()
            if valid_steps:
                next_step = valid_steps.pop()
                # if there's more than one valid step, save the others to explore later
                for step in valid_steps:
                    self.unexplored_paths.put({
                        'coords': tuple(self.coords),
                        'step': tuple(step),
                    })
            elif not self.unexplored_paths.empty():
                # if there are no valid steps, but there are saved states, start there instead
                saved_state = self.unexplored_paths.get()
                self.coords = np.array(saved_state['coords'])
                next_step = np.array(saved_state['step'])
            else:
                # if there are no valid steps or saved states, stop
                break
            self.coords += next_step


if __name__ == '__main__':
    test12a()
    print('Day 12a:', day12a('day12_input.txt'))
    test12b()
    print('Day 12b:', day12b('day12_input.txt'))
