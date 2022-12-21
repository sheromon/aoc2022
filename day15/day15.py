import numpy as np


def parse_input(input_path):
    data = []
    with open(input_path) as file_obj:
        for line in file_obj:
            if not line.strip():
                break
            assert line.startswith('Sensor at')
            sensor, beacon = line.strip().split(':')
            xy = sensor[len('Sensor at'):].strip().split(', ')
            sensor = [int(token[2:]) for token in xy]
            xy = beacon[len(' closest beacon is at'):].strip().split(', ')
            beacon = [int(token[2:]) for token in xy]
            data.append({
                'sensor': np.array(sensor),
                'beacon': np.array(beacon),
                'dist': np.abs(np.array(sensor) - np.array(beacon)).sum(),
            })
    return data


def day15a(input_path, row=2000000):
    """Return the number of positions in the specified row that cannot contain a beacon."""
    data = parse_input(input_path)
    eliminated_cols = set()
    beacon_cols = set()
    for item in data:
        dist = np.abs(item['sensor'] - item['beacon']).sum()
        sensor_col, sensor_row = item['sensor']
        beacon_col, beacon_row = item['beacon']
        if beacon_row == row:
            beacon_cols.add(beacon_col)

        extra_dist = dist - np.abs(sensor_row - row)
        if extra_dist < 0:
            continue
        new = set(list(range(sensor_col - extra_dist, sensor_col + extra_dist + 1)))
        eliminated_cols |= new
    eliminated_cols -= beacon_cols
    return len(eliminated_cols)


def test15a():
    assert 26 == day15a('test_input.txt', row=10)


def day15b(input_path, max_coord=4000000):
    """Return the tuning frequency for the distress beacon.

    The location of the distress beacon can be determined by process of elimination based on the locations of known
    pairs of sensors and their closest beacon.
    """
    data = parse_input(input_path)
    min_col = 0
    max_col = max_coord
    for row_ind in range(max_coord + 1):
        eliminated = np.zeros(max_coord + 1, dtype=bool)
        for item in data:
            beacon_dist = item['dist']
            row_dist = np.abs(item['sensor'][0] - row_ind)
            max_col_dist = beacon_dist - row_dist
            if max_col_dist <= 0:
                continue
            min_range = max(min_col, item['sensor'][1] - max_col_dist)
            max_range = min(max_col, item['sensor'][1] + max_col_dist)
            eliminated[min_range:max_range + 1] = 1
            if item['beacon'][0] == row_ind:
                eliminated[item['beacon'][1]] = 1
        col = np.argmin(eliminated)
        if eliminated[col]:
            continue
        tuning_freq = row_ind * 4000000 + col
        return tuning_freq


def test15b():
    assert 56000011 == day15b('test_input.txt', max_coord=20)


if __name__ == '__main__':
    test15a()
    print('Day 15a:', day15a('day15_input.txt'))
    test15b()
    print('Day 15b:', day15b('day15_input.txt'))
