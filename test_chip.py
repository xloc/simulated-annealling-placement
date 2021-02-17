import parser
import a2


def test_chip():
    ci = parser.Input(2, 2, 2, [[0, 1]])
    c = a2.Chip(ci)

    assert c.pins == [(0, 0), (0, 1), (1, 0), (1, 1)]

    assert c.grid
    assert False


def test_cost():
    nets = []

    n = a2.Net(0)
    # cost = 2
    n.pins.update([
        (0, 1), (0, 3)
    ])
    n.update_ltrb()
    nets.append(n)

    assert a2.calc_cost(nets) == 2

    n = a2.Net(1)
    # cost = 4
    n.pins.update([
        (1, 1), (3, 3)
    ])
    n.update_ltrb()
    nets.append(n)

    assert a2.calc_cost(nets) == 2 + 4
