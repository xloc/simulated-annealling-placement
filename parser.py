from collections import namedtuple

Input = namedtuple("Input", "nx ny n_cell nets")


def parse_file(path) -> Input:
    with open(path) as f:
        n_cell, n_net, ny, nx = [int(n) for n in f.readline().split()]

        nets = []
        for _ in range(n_net):
            line = f.readline().strip()
            if line == "":
                continue
            # print(repr(line))
            cell_IDs = line.split()[1:]
            cell_IDs = list(map(int, cell_IDs))
            nets.append(cell_IDs)

    return Input(nx, ny, n_cell, nets)


if __name__ == "__main__":
    input_path = 'benchmarks/cm138a.txt'
    result = parse_file(input_path)
    print(result)
