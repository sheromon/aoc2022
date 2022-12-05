from collections import defaultdict


def parse_input(input_path):
    """Return a dict of lists of crates by column, a list of move instructions, and the max crate column.

    Crates in a column are ordered with the bottom crate first.
    """
    max_col_num = 0
    with open(input_path) as file_obj:
        crates = defaultdict(list)
        for iline, line in enumerate(file_obj):
            found = False
            for ichar, char in enumerate(line):
                if char == '[':
                    found = True
                    letter = line[ichar + 1]
                    col_num = (ichar // 4) + 1
                    if col_num > max_col_num:
                        max_col_num = col_num
                    crates[col_num].append(letter)
            if not found:
                break
        moves = [line.strip() for line in file_obj]
        # rearrange crate list to go from bottom to top
        for key in crates:
            crates[key].reverse()
    return crates, moves, max_col_num


def day05a(input_path):
    """Return the top crate from each column at the end of the move instructions."""
    crates, moves, max_col_num = parse_input(input_path)
    for move in moves:
        tokens = move.split()
        if not tokens:
            continue
        num = int(tokens[1])
        from_col = int(tokens[3])
        to_col = int(tokens[-1])
        for _ in range(num):
            crate_to_move = crates[from_col].pop()
            crates[to_col].append(crate_to_move)
    result = []
    for num in range(1, max_col_num + 1):
        if crates[num]:
            result.append(crates[num][-1])
    return ''.join(result)


def test05a():
    assert 'CMZ' == day05a('test_input.txt')


def day05b(input_path):
    """Return the top crate from each column at the end of the move instructions (CrateMover 9001)."""
    crates, moves, max_col_num = parse_input(input_path)
    for move in moves[1:]:
        tokens = move.split()
        num = int(tokens[1])
        from_col = int(tokens[3])
        to_col = int(tokens[-1])
        crates_to_move = crates[from_col][-num:]
        crates[from_col] = crates[from_col][:-num]
        crates[to_col] += crates_to_move
    result = []
    for num in range(1, max_col_num + 1):
        if crates[num]:
            result.append(crates[num][-1])
    return ''.join(result)


def test05b():
    assert 'MCD' == day05b('test_input.txt')


if __name__ == '__main__':
    test05a()
    print('Day 05a:', day05a('day05_input.txt'))
    test05b()
    print('Day 05b:', day05b('day05_input.txt'))
