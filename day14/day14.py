import numpy as np


def parse_input(input_path):
    """Return a list of Nx2 numpy arrays, where array columns are x and y coordinates for rock formations.

    Each array defines a set of lines that makes up a single rock formation.
    """
    segments = []
    with open(input_path) as file_obj:
        for line in file_obj:
            points = []
            for xy in line.strip().split('->'):
                points.append([int(val) for val in xy.split(',')])
            segments.append(np.array(points))
    return segments


class Cave:
    """Capture layout of cave, including rock formations and sand."""

    def __init__(self, segments):
        self.sand_escaped = False  # becomes True when sand starts falling into the abyss
        self.sand_blocked = False  # becomes True when the entry point for sand is blocked
        mins = np.min(np.stack([np.min(seg, axis=0) for seg in segments]), axis=0)
        maxs = np.max(np.stack([np.max(seg, axis=0) for seg in segments]), axis=0)
        height = maxs[1] + 3
        width = maxs[0] - mins[0] + 2 * height
        self.array = np.array(height * [width * ['.']])  # grid of empty (.), rock (#), and sand (o) positions
        self.x_offset = mins[0] - height  # x-coordinate adjustment
        self.entry_xy = np.array([500 - self.x_offset, 0])

        # set up rock formations
        for seg in segments:
            seg[:, 0] -= self.x_offset
            for ind in range(len(seg) - 1):
                min_xy = np.min(seg[ind:ind + 2], axis=0)
                max_xy = np.max(seg[ind:ind + 2], axis=0)
                self.array[min_xy[1]:max_xy[1] + 1, min_xy[0]:max_xy[0] + 1] = '#'

    def add_floor(self):
        """Add in rock representing the cave floor (part 2 only)."""
        self.array[-1, :] = '#'

    def __str__(self):
        return '\n'.join((''.join(row) for row in self.array))

    def drop_sand(self, start_x, start_y):
        """Simulate a grain of sand falling until either it comes to rest or we determine it will not."""
        done = False
        while not done:
            next_y = np.argmax(self.array[start_y:, start_x] != '.') - 1 + start_y
            if (next_y < start_y) or (start_x == 0) or (start_x == self.array.shape[1] - 1):
                self.sand_escaped = True  # sand is going to fall into the abyss
                return
            if self.array[next_y + 1, start_x - 1] == '.':
                start_x -= 1
                start_y = next_y + 1
            elif self.array[next_y + 1, start_x + 1] == '.':
                start_x += 1
                start_y = next_y + 1
            else:
                self.array[next_y, start_x] = 'o'
                if (start_x == self.entry_xy[0]) and (next_y == self.entry_xy[1]):
                    self.sand_blocked = True
                done = True


def day14a(input_path):
    """Return the number of grains of sand that come to rest on the rock formations."""
    segments = parse_input(input_path)
    cave = Cave(segments)

    sand_xy = np.array([500 - cave.x_offset, 0])
    num_sand = 0
    while True:
        cave.drop_sand(start_x=sand_xy[0], start_y=sand_xy[1])
        if cave.sand_escaped:
            break
        num_sand += 1
    return num_sand


def test14a():
    assert 24 == day14a('test_input.txt')


def day14b(input_path):
    """Return the number of grains of sand that are able to fall into the cave."""
    segments = parse_input(input_path)
    cave = Cave(segments)
    cave.add_floor()

    sand_xy = np.array([500 - cave.x_offset, 0])
    num_sand = 0
    while not cave.sand_blocked:
        cave.drop_sand(start_x=sand_xy[0], start_y=sand_xy[1])
        num_sand += 1
    return num_sand


def test14b():
    assert 93 == day14b('test_input.txt')


if __name__ == '__main__':
    test14a()
    print('Day 14a:', day14a('day14_input.txt'))
    test14b()
    print('Day 14b:', day14b('day14_input.txt'))
