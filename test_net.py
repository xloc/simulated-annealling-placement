from net import Net


def test_update_ltrb():
    n = Net(1)
    n.pins.update([
        (1, 2), (3, 4), (1, 5), (9, 3)
    ])
    n.update_ltrb()

    assert n.cost == 11


def test_update_ltrb_one_pin():
    n = Net(1)
    n.pins.update([
        (1, 2)
    ])
    n.update_ltrb()

    assert n.cost == 0
