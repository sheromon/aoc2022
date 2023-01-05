import itertools

import numpy as np


SHAPES = ('-', '+', 'L', '|', 'x')


def day17a(input_path):
    """Return the height of the rock tower after 2022 rocks have fallen."""
    jets_iter = itertools.cycle(parse_input(input_path))
    shapes_iter = itertools.cycle(SHAPES)
    room = Room(room_height=2000 * 4)

    for num_rock in range(2022):
        rock = Rock(next(shapes_iter), room.max_height)
        while not rock.stopped:
            direction = next(jets_iter)
            if direction == '<':
                push_rock_left(rock, room)
            elif direction == '>':
                push_rock_right(rock, room)
            move_rock_down(rock, room)
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


def push_rock_left(rock, room):
    if rock.shape == '+':
        check = np.append(
            room.array[rock.bottom:rock.bottom + rock.height, rock.left],
            room.array[rock.bottom + 1, rock.left - 1],
        )
    elif rock.shape == 'L':
        check = np.append(
            room.array[rock.bottom:rock.bottom + rock.height, rock.left],
            room.array[rock.bottom, rock.left - 1],
        )
    else:
        check = room.array[rock.bottom:rock.bottom + rock.height, rock.left - 1]
    rock.left -= 1 * np.all(check == 0)


def push_rock_right(rock, room):
    if rock.shape == '+':
        check = np.append(
            room.array[rock.bottom:rock.bottom + rock.height, rock.left + rock.width - 1],
            room.array[rock.bottom + 1, rock.left + rock.width],
        )
    else:
        check = room.array[rock.bottom:rock.bottom + rock.height, rock.left + rock.width]
    rock.left += 1 * np.all(check == 0)


def move_rock_down(rock, room):
    if rock.shape == '+':
        check = np.append(
            room.array[rock.bottom, rock.left:rock.left + rock.width],
            room.array[rock.bottom - 1, rock.left + 1],
        )
    else:
        check = room.array[rock.bottom - 1, rock.left:rock.left + rock.width]
    if np.any(check):
        freeze_rock_in_room(rock, room)
        return
    rock.bottom -= 1


def freeze_rock_in_room(rock, room):
    rock.stopped = True
    if rock.shape in ('-', '|', 'x'):
        room.array[rock.bottom:rock.bottom + rock.height, rock.left:rock.left + rock.width] = 1
    elif rock.shape == '+':
        room.array[rock.bottom + 1, rock.left:rock.left + rock.width] = 1
        room.array[rock.bottom:rock.bottom + rock.height, rock.left + 1] = 1
    elif rock.shape == 'L':
        room.array[rock.bottom, rock.left:rock.left + rock.width] = 1
        room.array[rock.bottom:rock.bottom + rock.height, rock.left + 2] = 1
    room.max_height = max(room.max_height, rock.bottom + rock.height - 1)


class Room:

    def __init__(self, room_height=20):
        room_width = 9
        self.array = np.zeros((room_height, room_width), int)
        self.array[0, :] = 1
        self.array[:, 0] = 1
        self.array[:, -1] = 1
        self.max_height = 0

    def __str__(self):
        char_array = np.flipud(self.array).astype('U1')
        char_array[char_array == '1'] = '#'
        char_array[char_array == '0'] = '.'
        return '\n'.join([''.join([char for char in row]) for row in char_array.tolist()])


def test17a():
    assert 3068 == day17a('test_input.txt')


def day17b(input_path):
    pass


def test17b():
    assert 1707 == day17b('test_input.txt')


if __name__ == '__main__':
    test17a()
    print('Day 17a:', day17a('day17_input.txt'))
    # test17b()
    # print('Day 17b:', day17b('day17_input.txt'))
