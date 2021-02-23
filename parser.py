from collections import namedtuple

Input = namedtuple("Input", "nx ny n_cell nets")


def parse_file(path) -> Input:
    with open(path) as f:
        n_cell, n_net, ny, nx = [int(n) for n in f.readline().split()]

        nets = []
        i_net = 0
        while True:
            line = f.readline().strip()
            if line == "":
                continue
            # print(repr(line))
            cell_IDs = line.split()[1:]
            cell_IDs = list(map(int, cell_IDs))
            nets.append(cell_IDs)

            i_net += 1
            if not i_net < n_net:
                break

    return Input(nx, ny, n_cell, nets)


if __name__ == "__main__":
    input_path = 'benchmarks/cm138a.txt'
    result = parse_file(input_path)
    print(result)
