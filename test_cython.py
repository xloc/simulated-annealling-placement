import pytest
import a2
import io
import parser


def build_chip(Net_, n_net, mat):
    nets = []
    for i in range(n_net):
        nets.append(Net_(i))

    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] is None:
                cell = []
            elif not isinstance(mat[i][j], list):
                cell = [mat[i][j]]

            for k in range(len(cell)):
                nets[0].pins.add((i, j))
            mat[i][j] = cell
    for net in nets:
        net.update_ltrb()
    return nets, mat


def test_net_cost_python():
    _ = None
    nets, grid = build_chip(
        a2.import_Net(use_cython=False), 1,
        [
            [_, 0, _],
            [0, _, 0]
        ])

    assert nets[0].cost == 3


def test_net_cost_cython():
    _ = None
    nets, grid = build_chip(
        a2.import_Net(use_cython=True), 1,
        [
            [_, 0, _],
            [0, _, 0]
        ])

    assert nets[0].cost == 3
