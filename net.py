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
