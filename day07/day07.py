

def parse_input(input_path):
    with open(input_path) as file_obj:
        lines = [line.strip() for line in file_obj]
    return lines


def day07a(input_file):
    """Return the total sizes of all directories with total size <= 100000."""
    lines = parse_input(input_file)
    top_dir, all_dirs = map_directories(lines)
    calc_sizes(top_dir, all_dirs)
    return sum(d.total_size for d in all_dirs if d.total_size <= 100000)


def test07a():
    assert 95437 == day07a('test_input.txt')


def day07b(input_file):
    """Return the size of the smallest directory that can be deleted to free up the needed amount of space."""
    total_space = 70000000
    required = 30000000

    lines = parse_input(input_file)
    top_dir, all_dirs = map_directories(lines)
    calc_sizes(top_dir, all_dirs)

    used = top_dir.total_size
    available = total_space - used
    more_needed = required - available

    return min(d.total_size for d in all_dirs if d.total_size >= more_needed)


def test07b():
    assert 24933642 == day07b('test_input.txt')


class Directory:

    def __init__(self, name, parent=None):
        self.name = name
        self.files = {}
        self.subdirs = {}
        self.total_size = None
        self.parent = parent

    def __str__(self):
        output = f'{self.name} (size={self.total_size or "unknown"})\n'
        for name, size in self.files.items():
            output += f'  {name} (file, size={size})\n'
        for name, subdir in self.subdirs.items():
            output += f'  {name} (dir, size={subdir.total_size or "unknown"})\n'
        return output


def map_directories(lines):
    """Use recorded commands and output to map out directory structure.

    :return: tuple(top_dir, all_dirs), where top_dir is a Directory corresponding to the root directory, and all_dirs
        is a set of all Directory objects
    """
    current_dir = None
    top_dir = Directory('/')
    all_dirs = {top_dir}

    lines.reverse()
    line = lines.pop()
    tokens = line.split()
    while lines:
        assert tokens[0] == '$'
        command = tokens[1]
        if command == 'cd':
            dest = tokens[2]
            if dest == '/':
                current_dir = top_dir
            elif dest == '..':
                current_dir = current_dir.parent
            else:
                subdir = current_dir.subdirs.get(dest)
                if not subdir:
                    subdir = Directory(dest, parent=current_dir)
                    all_dirs.add(subdir)
                current_dir = subdir
            tokens = lines.pop().split()
        elif command == 'ls':
            tokens = lines.pop().split()
            while tokens[0] != '$':
                name = tokens[1]  # file or subdir name
                if tokens[0] == 'dir':
                    subdir = Directory(name, parent=current_dir)
                    all_dirs.add(subdir)
                    current_dir.subdirs[name] = subdir
                else:
                    size = int(tokens[0])
                    current_dir.files[name] = size
                if not lines:
                    break
                tokens = lines.pop().split()
        else:
            raise RuntimeError(f"Invalid command '{command}'.")

    return top_dir, all_dirs


def calc_sizes(top_dir, all_dirs):
    """Given the root directory and a set of all directories, calculate total sizes for all directories."""
    # identify lowest subirs (ones that have no subdirs themselves), and calculate their sizes
    current_dirs = set()
    for d in all_dirs:
        if d.total_size:
            continue
        elif not d.subdirs:
            d.total_size = sum(d.files.values())
            current_dirs.add(d)

    # from the bottom dirs, try to calculate sizes for their parent dirs until we reach the top
    while not top_dir.total_size:
        next_dirs = set()
        for d in current_dirs:
            parent = d.parent
            if parent.total_size:
                continue
            try:
                parent.total_size = sum(parent.files.values()) + sum(d.total_size for d in parent.subdirs.values())
                next_dirs.add(parent)
            except TypeError:
                # if any of the parent's subdirs do not have total size, the calculation is impossible now
                # but we will get it later
                continue
        current_dirs = next_dirs


if __name__ == '__main__':
    test07a()
    print('Day 07a:', day07a('day07_input.txt'))
    test07b()
    print('Day 07b:', day07b('day07_input.txt'))
