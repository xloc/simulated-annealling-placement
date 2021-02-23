import pyximport
pyximport.install()  # noqa

import numpy as np
import parser
import random
from typing import List
import math
import matplotlib.pyplot as plt


class Net:
    __slots__ = tuple('id pins cost'.split())

    def __init__(self, netID):
        self.id = netID
        self.pins = set()
        self.cost = 0

    def update_ltrb(self):
        i_pin = iter(self.pins)
        x, y = next(i_pin)
        t, b = y, y
        l, r = x, x

        for x, y in i_pin:
            if x < l:
                l = x
            elif x > r:
                r = x
            if y < t:
                t = y
            elif y > b:
                b = y

        self.cost = (r - l) + (b - t)

    def __repr__(self):
        return f"<Net id={self.id}>"


# from net import Net  # noqa


class Grid:
    def __init__(self, nx, ny):
        self.grid = [[None]*nx for _ in range(ny)]
        self.shape = (nx, ny)

    def __getitem__(self, xy):
        x, y = xy
        return self.grid[y][x]

    def __setitem__(self, xy, val):
        x, y = xy
        self.grid[y][x] = val

    def format_print(self, min_space, cell_formatter):
        nx, ny = self.shape
        for y in range(ny):
            print(','.join([
                f"{cell_formatter(self[x, y]):{min_space}s}"
                for x in range(nx)
            ]))


class Chip:
    def __init__(self, chip_info: parser.Input):
        self.ny = ny = chip_info.ny
        self.nx = nx = chip_info.nx
        self.shape = (nx, ny)
        self.n_cell = chip_info.n_cell

        self.pins = []
        for x in range(chip_info.nx):
            for y in range(chip_info.ny):
                self.pins.append((x, y))

        # Random Cell to Coordinate assignment
        cid2xy = list(self.pins)
        random.shuffle(cid2xy)
        cid2xy = cid2xy[:chip_info.n_cell]
        # print(cid2xy)

        # Place into grid
        self.grid = Grid(nx, ny)
        self.nets = []
        for net_ID, cell_IDs in enumerate(chip_info.nets):
            net = Net(net_ID)
            self.nets.append(net)
            # print(cell_IDs)
            for cid in cell_IDs:
                cx, cy = cid2xy[cid]
                net.pins.add((cx, cy))
                if self.grid[cx, cy] is None:
                    self.grid[cx, cy] = set([net])
                else:
                    self.grid[cx, cy].add(net)
            net.update_ltrb()

    def cost(self):
        return sum(net.cost for net in self.nets)

    def detach_cell(self, coors):
        cell = self.grid[coors]
        if cell is None:
            return None

        self.grid[coors] = None
        for net in cell:
            net.pins.remove(coors)
            # Note: cell will always been attached to another coors, so the ltrb is not updated here
            # net.update_ltrb()
        return cell

    def attach_cell(self, cell, coors):
        assert self.grid[coors] is None, "Cannot attach cell to non-empty coors"
        if cell is None:
            return

        for net in cell:
            net.pins.add(coors)
            net.update_ltrb()
        self.grid[coors] = cell

    def swap_cell(self, a, b):
        ca, cb = self.detach_cell(a), self.detach_cell(b)
        self.attach_cell(ca, b)
        self.attach_cell(cb, a)

    def plot(self, ax):
        nets = self.nets
        for net in nets:
            arr = np.array(list(net.pins))
            x, y = arr[:, 0], arr[:, 1]
            ax.plot(x, y, color=[0, 0, 0, 0.3])
        ax.set_xlim([0, self.nx-1])
        ax.set_ylim([0, self.ny-1])

    def cell_cost(self, coord):
        """
        the bounding box of all nets in the cell should **already** be updated.
        """
        cell = self.grid[coord]
        if cell is None:
            return 0
        else:
            return sum(net.cost for net in cell)


def move(cell, src, dst):
    cell = list(cell)
    moved_cell = []
    for net in cell:
        moved_net = net.copy()
        moved_net.pins.remove(src)
        moved_net.pins.add(dst)
        moved_net.update_ltrb()
        moved_cell.append(moved_net)
    return moved_cell


def annealing_placement(chip: Chip, t_init=100, t_decrease_factor=0.5, t_terminate=0.01):
    t = t_init
    i_iter = 0
    n_batch = int(100 * chip.n_cell ** (4/3))

    def decrease_t(pt):
        return pt * t_decrease_factor

    def should_terminate():
        if t < t_terminate:
            return True

    acc_delta = 0
    yield chip, dict(acc_delta=acc_delta, t=t, i_iter=i_iter)

    while True:
        acc_delta = 0

        for _ in range(n_batch):
            a, b = random.sample(chip.pins, k=2)

            prev_cost = chip.cell_cost(a) + chip.cell_cost(b)
            chip.swap_cell(a, b)
            curr_cost = chip.cell_cost(a) + chip.cell_cost(b)
            delta = curr_cost - prev_cost

            r = random.random()
            if r < math.exp(-delta/t):  # confirm swap
                acc_delta += delta
            else:  # restore swap
                chip.swap_cell(a, b)

        yield chip, dict(acc_delta=acc_delta, t=t, i_iter=i_iter)

        i_iter += 1
        t = decrease_t(t)
        if should_terminate():
            break


def nets_formatter(cell: set):
    if cell:
        return ' '.join([str(net.id) for net in cell])
    else:
        return ''


def formatter(cell):
    if cell:
        return 'x'
    else:
        return ''

# chip_info = parser.parse_file(file_path)
# c = Chip(chip_info)
# print(c.nx, c.ny)
# print(chip_info.n_cell)
# print(chip_info.nets)
# pins = set()
# for net in chip_info.nets:
#     pins.update(net)
# print(sorted(list(pins)))
# print(set(range(chip_info.n_cell)) - pins)
# c.grid.format_print(3, formatter)
