import parser
import a2
from net import Net


def test_chip():
    import random
    random.seed(1)

    ci = parser.Input(2, 2, 2, [[0, 1]])
    c = a2.Chip(ci, Net)

    assert c.pins == [(0, 0), (0, 1), (1, 0), (1, 1)]
    c.grid.format_print(8, a2.nets_formatter)
    assert c.grid[0, 0] == {c.nets[0]}
    assert c.grid[1, 1] == {c.nets[0]}


def test_cell_cost():
    import random
    random.seed(1)

    ci = parser.Input(3, 2, 3, [[0, 1], [1, 2]])
    c = a2.Chip(ci, Net)

    # c.grid.format_print(8, a2.nets_formatter)
    assert c.cell_cost((1, 0)) == 1
    assert c.cell_cost((1, 1)) == 2
    assert c.cell_cost((2, 1)) == 1
