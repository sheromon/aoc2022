

def parse_input(input_path):
    instructions = []
    with open(input_path) as file_obj:
        for line in file_obj:
            tokens = line.strip().split()
            instructions.append(tokens)
    return instructions


class ClockCircuitAnalyzer:
    """ClockCircuitAnalyzer iterates through instructions and keeps track of the current and next states."""

    def __init__(self, input_path):
        instructions = parse_input(input_path)
        instructions.reverse()  # reverse instructions so that we can pop them off later
        self.instructions = instructions
        self.prev_cycle = 0
        self.next_cycle = 0
        self.x = 1  # x starts at 1
        self.next_x = 1

    def advance(self):
        # update x and cycle to previously calculated value
        self.x = self.next_x
        self.prev_cycle = self.next_cycle

        # try to get the next instruction
        try:
            instruction = self.instructions.pop()
        except IndexError:
            # if we're out of instructions, just increment the cycle and exit
            self.next_cycle += 1
            return

        # parse the instruction to figure out what the cycle and value of x will be next
        if instruction[0] == 'noop':
            self.next_cycle += 1
        elif instruction[0] == 'addx':
            self.next_cycle += 2
            self.next_x += int(instruction[1])
        else:
            raise RuntimeError(f"Invalid instruction '{instruction[0]}'")


def day10a(input_path):
    """Return the sum of the signal strengths at cycle 20 and every 40 later cycles through cycle 220."""
    stops = list(range(20, 221, 40))
    stops.append(stops[-1])
    stops.reverse()
    stop = stops.pop()

    signal_strengths = []
    c = ClockCircuitAnalyzer(input_path)
    while stops:
        while stops and (c.prev_cycle < stop <= c.next_cycle):
            # signal strength is current cycle times current value of x
            signal_strengths.append(stop * c.x)
            stop = stops.pop()
        c.advance()
    return sum(signal_strengths)


def test10a():
    assert 13140 == day10a('test_input.txt')


def day10b(input_path):
    """Print out the screen after 240 cycles."""
    stops = list(range(1, 242))  # I kind of want to do a generator instead
    stops.reverse()
    this_cycle = stops.pop()

    screen = ''
    row = ''
    row_length = 40
    c = ClockCircuitAnalyzer(input_path)
    while c.prev_cycle < 242:
        while stops and (c.prev_cycle < this_cycle <= c.next_cycle):
            # x gives the center of the sprite position, and the sprite is 3 pixels wide
            sprite_min = c.x - 1
            sprite_max = c.x + 1
            # if current pixel position intersects with sprite position, print #, else print .
            pixel_pos = (this_cycle - 1) % row_length
            if sprite_min <= pixel_pos <= sprite_max:
                row += '#'
            else:
                row += '.'
            if this_cycle % row_length == 0:
                screen += row + '\n'
                row = ''
            this_cycle = stops.pop()
        c.advance()

    return screen


def test10b():
    expected = '\n'.join([
        '##..##..##..##..##..##..##..##..##..##..',
        '###...###...###...###...###...###...###.',
        '####....####....####....####....####....',
        '#####.....#####.....#####.....#####.....',
        '######......######......######......####',
        '#######.......#######.......#######.....',
        '',
    ])
    assert expected == day10b('test_input.txt')


if __name__ == '__main__':
    test10a()
    print('Day 10a:', day10a('day10_input.txt'))
    test10b()
    print('Day 10b:')
    print(day10b('day10_input.txt'))
