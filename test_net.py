from a2 import Net


def test_update_ltrb():
    n = Net(1)
    n.pins.update([
        (1, 2), (3, 4), (1, 5), (9, 3)
    ])
    n.update_ltrb()

    assert n.lt == (1, 2)
    assert n.rb == (9, 5)


def test_update_ltrb_one_pin():
    n = Net(1)
    n.pins.update([
        (1, 2)
    ])
    n.update_ltrb()

    assert n.lt == (1, 2)
    assert n.rb == (1, 2)
