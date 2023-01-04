

def day16a(input_path):
    """Return the maximum units of pressure that can be released in 30 minutes by opening a sequence of valves."""
    valves = parse_input(input_path)
    # we only care about opening valves that have a nonzero flow rate
    valve_name_list = [name for name, valve in valves.items() if valve.rate > 0]

    evaluator = Evaluator(valves, valve_name_list)

    total_pressure_list = []
    # the total pressure released is a function of which valves are opened in what order, so we will calculate the total
    # pressure for various sequences of valves being opened, starting with sequences of length one
    next_sequences = [[name] for name in valve_name_list]
    while next_sequences:
        sequences = next_sequences
        # next round of sequences will be sequences that could be completed this round plus one additional valve
        next_sequences = []
        for sequence in sequences:
            completed, total = evaluator.evaluate_valve_sequence(sequence)
            if completed:
                next_valve_choices = set(valve_name_list) - set(sequence)
                next_sequences += [sequence + [next_valve] for next_valve in next_valve_choices]
            total_pressure_list.append(total)
    return max(total_pressure_list)


def parse_input(input_path):
    """Parse the input file and return a dictionary of valve names to Valve objects."""
    valves = {}
    with open(input_path) as file_obj:
        for line in file_obj:
            line = line.strip()
            if not line:
                break
            valve_info, tunnel_info = line.split(';')
            tokens = valve_info.split()
            valve_name = tokens[1]
            rate = int(tokens[-1].split('=')[-1])
            connections = [c.strip() for c in tunnel_info[len('tunnels lead to valves '):].split(',')]
            valves[valve_name] = Valve(name=valve_name, rate=rate, connections=connections)
    return valves


class Valve:
    """Store basic information about a valve."""

    def __init__(self, name, rate, connections):
        self.name = name
        self.rate = rate
        self.connections = connections

    def __repr__(self):
        return str(self.__dict__)


class DistanceMap:
    """Store dictionaries that allow quick lookup of minimum distances between pairs of valves."""

    def __init__(self, valves, valve_name_list):
        self.from_map = dict()
        for valve_name in valve_name_list:
            self._calc_distances(valves, valve_name)

    def get_min_distance(self, from_name, to_name):
        """Return the minimum number of steps between two valves."""
        return self.from_map[from_name][to_name]

    def _calc_distances(self, valves, from_valve):
        """Calculate the minimum distance from one valve to all other valves and return the results as a dictionary."""

        def recursive_distance(dist_map, valve, min_dist):
            for name in valve.connections:
                if name not in dist_map or min_dist < dist_map[name]:
                    dist_map[name] = min_dist
                    recursive_distance(dist_map, valves[name], min_dist + 1)

        self.from_map[from_valve] = {from_valve: 0}
        recursive_distance(self.from_map[from_valve], valves[from_valve], 1)


class Evaluator:

    def __init__(self, valves, nonzero_valve_names):
        self.valves = valves
        # pre-calculate min distances from each valve of interest (plus starting valve) to all other valves
        self.distance_map = DistanceMap(valves, nonzero_valve_names + ['AA'])

    def evaluate_valve_sequence(self, sequence, max_time=30):
        """Determine whether a sequence of valves can all be opened within the time limit and the pressure released."""
        current_valve_name = 'AA'
        total = 0
        minutes_remaining = max_time
        completed = True
        for ind, valve_name in enumerate(sequence):
            steps = self.distance_map.get_min_distance(current_valve_name, valve_name)
            if steps > minutes_remaining:
                completed = False
                break
            minutes_remaining -= steps + 1
            total += minutes_remaining * self.valves[valve_name].rate
            current_valve_name = valve_name
        # what we really care about is if we had enough time to open all valves in this sequence and then open another
        # valve after that, so add a check on time remaining
        completed = completed and minutes_remaining > 2
        return completed, total


def test16a():
    assert 1651 == day16a('test_input.txt')


def day16b(input_path):
    """Return the maximum units of pressure that can be released in 26 minutes by opening valves with help."""
    valves = parse_input(input_path)
    # we only care about opening valves that have a nonzero flow rate
    valve_name_list = [name for name, valve in valves.items() if valve.rate > 0]

    evaluator = Evaluator(valves, valve_name_list)

    # this time, record all sequences checked with corresponding pressure released
    total_pressure_map = {}
    # the total pressure released is a function of which valves are opened in what order, so we will calculate the total
    # pressure for various sequences of valves being opened, starting with sequences of length one
    next_sequences = [[name] for name in valve_name_list]
    while next_sequences:
        sequences = next_sequences
        # next round of sequences will be sequences that could be completed this round plus one additional valve
        next_sequences = []
        for sequence in sequences:
            completed, total = evaluator.evaluate_valve_sequence(sequence, max_time=26)
            if completed:
                next_valve_choices = set(valve_name_list) - set(sequence)
                next_sequences += [sequence + [next_valve] for next_valve in next_valve_choices]
            total_pressure_map[tuple(sequence)] = total

    # sort sequences from most to least pressure released
    pressure_list = sorted(total_pressure_map.items(), key=lambda x: x[1], reverse=True)

    # check pairs of sequences starting from highest total values
    max_total_pressure = 0
    max_ind = 2
    while max_ind < len(pressure_list) - 1:
        for ind in range(max_ind - 1):
            seq0 = pressure_list[ind][0]
            seq1 = pressure_list[max_ind][0]
            # if the two sequences share any valves, the result is invalid
            if set(seq0) & set(seq1):
                continue
            total_pressure = pressure_list[ind][1] + pressure_list[max_ind][1]
            max_total_pressure = max(max_total_pressure, total_pressure)
        max_ind += 1
        # stop checking sequences when we think we've probably found the highest valid total
        if pressure_list[max_ind][1] < max_total_pressure * 0.4:
            break
    return max_total_pressure


def test16b():
    assert 1707 == day16b('test_input.txt')


if __name__ == '__main__':
    test16a()
    print('Day 16a:', day16a('day16_input.txt'))
    test16b()
    print('Day 16b:', day16b('day16_input.txt'))
