import parser
import a2
from a2 import (
    Chip, swap_cell
)
import random
import math


def cell_cost(cell):
    if cell is None:
        return 0
    cost = 0
    for net in cell:
        cost += net.cost()
    return cost


def annealing_placement(chip: Chip):
    t = 5

    def decrease(pt):
        return pt * 0.9
    n_batch = int(100 * chip.n_cell ** (4/3))

    i_iter = 0

    def criteria():
        nonlocal i_iter
        if t < 0.5:
            return True

    while True:
        acc_delta = 0
        print("%10d" % chip.cost())
        for i_iter in range(n_batch):
            # chip.grid.format_print(10, nets_formatter)
            # print('==='*10)
            # print(chip.cost())
            a, b = random.sample(chip.pins, k=2)

            prev_cost = cell_cost(chip.grid[a]) + cell_cost(chip.grid[b])
            swap_cell(chip, a, b)
            curr_cost = cell_cost(chip.grid[a]) + cell_cost(chip.grid[b])
            delta = curr_cost - prev_cost

            r = random.random()
            if r < math.exp(-delta/t):
                # if delta < 0:
                # do swap
                pass
                acc_delta += delta
            else:
                # restore swap
                swap_cell(chip, a, b)

        print("%.2f" % t, acc_delta)
        t = decrease(t)
        if criteria():
            break


random.seed(12)
chip_info = parser.parse_file('benchmarks/apex1.txt')
chip = a2.Chip(chip_info)

# chip.grid.format_print(10, a2.nets_formatter)

annealing_placement(chip)
