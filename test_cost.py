import pytest
import a2
import io
import parser


def build_chip(n_net, mat):
    nets = []
    for i in range(n_net):
        nets.append(a2.Net(i))

    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] is None:
                cell = []
            elif not isinstance(mat[i][j], list):
                cell = [mat[i][j]]

            for k in range(len(cell)):
                cell[k] = nets[cell[k]]
            mat[i][j] = cell
    return nets, mat


def test_calc_net_cost():
    _ = None
    nets, grid = build_chip(1, [
        [_, 0, _],
        [0, _, _]
    ])

    a2.calc_net_cost(nets[0])
