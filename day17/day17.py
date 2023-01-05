import itertools

import numpy as np


SHAPES = ('-', '+', 'L', '|', 'x')


def day17a(input_path):
    """Return the height of the rock tower after 2022 rocks have fallen."""
    room = Room(input_path, room_height=2000 * 4)
    room.run_rock_sim(num_rocks=2022)
    return room.max_height


def parse_input(input_path):
    """Return the string from the input file."""
    with open(input_path) as file_obj:
        return file_obj.read().strip()


class Rock:

    def __init__(self, shape, max_room_height):
        if shape not in SHAPES:
            raise ValueError(f"Shape must be one of {SHAPES} but got {shape}.")
        self.shape = shape
        size_map = {
            '-': (4, 1),
            '+': (3, 3),
            'L': (3, 3),
            '|': (1, 4),
            'x': (2, 2),
        }
        self.width, self.height = size_map[shape]
        self.left = 3  # rocks start two units away from the left wall
        self.bottom = max_room_height + 4  # rocks start three units above the highest rock or the floor
        self.stopped = False

    def __repr__(self):
        return str(self.__dict__)


class Room:

    def __init__(self, input_path, room_height=20):
        self.jets_iter = itertools.cycle(parse_input(input_path))
        self.shapes_iter = itertools.cycle(SHAPES)
        room_width = 9  # room is 7 units wide, but add 2 for the walls
        # the rock layout is represented by the array; 1 is fixed rock; 0 is empty space
        self.array = np.zeros((room_height, room_width), int)
        self.array[0, :] = 1  # make the floor solid rock
        self.array[:, 0] = 1  # left wall
        self.array[:, -1] = 1  # right wall
        self.max_height = 0  # keep track of max height of rock tower (0 for bare floor)
        self.num_rocks = 0  # keep track of the number of rocks that have fallen

    def __str__(self):
        char_array = np.flipud(self.array).astype('U1')
        char_array[char_array == '1'] = '#'
        char_array[char_array == '0'] = '.'
        return '\n'.join([''.join([char for char in row]) for row in char_array.tolist()])

    def run_rock_sim(self, num_rocks):
        """Simulate the specified number of rocks falling in sequence."""
        for num_rock in range(num_rocks):
            rock = Rock(next(self.shapes_iter), self.max_height)
            while not rock.stopped:
                direction = next(self.jets_iter)
                if direction == '<':
                    self.push_rock_left(rock)
                elif direction == '>':
                    self.push_rock_right(rock)
                self.move_rock_down(rock)

    def push_rock_left(self, rock):
        if rock.shape == '+':
            check = np.append(
                self.array[rock.bottom:rock.bottom + rock.height, rock.left],
                self.array[rock.bottom + 1, rock.left - 1],
            )
        elif rock.shape == 'L':
            check = np.append(
                self.array[rock.bottom:rock.bottom + rock.height, rock.left],
                self.array[rock.bottom, rock.left - 1],
            )
        else:
            check = self.array[rock.bottom:rock.bottom + rock.height, rock.left - 1]
        rock.left -= 1 * np.all(check == 0)

    def push_rock_right(self, rock):
        if rock.shape == '+':
            check = np.append(
                self.array[rock.bottom:rock.bottom + rock.height, rock.left + rock.width - 1],
                self.array[rock.bottom + 1, rock.left + rock.width],
            )
        else:
            check = self.array[rock.bottom:rock.bottom + rock.height, rock.left + rock.width]
        rock.left += 1 * np.all(check == 0)

    def move_rock_down(self, rock):
        if rock.shape == '+':
            check = np.append(
                self.array[rock.bottom, rock.left:rock.left + rock.width],
                self.array[rock.bottom - 1, rock.left + 1],
            )
        else:
            check = self.array[rock.bottom - 1, rock.left:rock.left + rock.width]
        if np.any(check):
            self.freeze_rock(rock)
            return
        rock.bottom -= 1

    def freeze_rock(self, rock):
        """When a rock cannot fall further, indicate that it has stopped, and make it part of the room's fixed rock."""
        rock.stopped = True
        self.num_rocks += 1
        if rock.shape in ('-', '|', 'x'):
            self.array[rock.bottom:rock.bottom + rock.height, rock.left:rock.left + rock.width] = 1
        elif rock.shape == '+':
            self.array[rock.bottom + 1, rock.left:rock.left + rock.width] = 1
            self.array[rock.bottom:rock.bottom + rock.height, rock.left + 1] = 1
        elif rock.shape == 'L':
            self.array[rock.bottom, rock.left:rock.left + rock.width] = 1
            self.array[rock.bottom:rock.bottom + rock.height, rock.left + 2] = 1
        self.max_height = max(self.max_height, rock.bottom + rock.height - 1)


def test17a():
    assert 3068 == day17a('test_input.txt')


def day17b(input_path):
    """Return the height of the rock tower after 1000000000000 rocks have fallen."""
    desired_num_rocks = 1000000000000

    room = Room(input_path, room_height=2000 * 4)
    # run for some amount of time to warm up
    room.run_rock_sim(num_rocks=2000)

    # run for a bunch more steps
    max_heights = []
    # 40 is the length of the jet pattern in the test input, but it seems to work for the real input too
    for num_rock in range(40):
        room.run_rock_sim(num_rocks=1)
        max_heights.append(room.max_height)
    max_height_deltas = np.diff(np.array(max_heights))
    prev_num_rocks = room.num_rocks
    prev_max_height = max_heights[-1]

    # keep running until the pattern repeats
    found = False
    while not found:
        room.run_rock_sim(num_rocks=1)
        max_heights = max_heights[1:] + [room.max_height]
        if np.all(max_height_deltas == np.diff(np.array(max_heights))):
            break

    # derive the length of the pattern, how many more full cycles are needed, and how many steps we need to get to the
    # desired number of rocks in addition to the full cycles
    cycle_length = room.num_rocks - prev_num_rocks
    added_height = room.max_height - prev_max_height
    num_cycles_more = (desired_num_rocks - room.num_rocks) // cycle_length
    rocks_to_add = desired_num_rocks - num_cycles_more * cycle_length - room.num_rocks

    room.run_rock_sim(num_rocks=rocks_to_add)
    return room.max_height + num_cycles_more * added_height


def test17b():
    assert 1514285714288 == day17b('test_input.txt')


if __name__ == '__main__':
    test17a()
    print('Day 17a:', day17a('day17_input.txt'))
    test17b()
    print('Day 17b:', day17b('day17_input.txt'))
