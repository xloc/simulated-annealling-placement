cdef class Net:
    cdef int id
    cdef public int cost
    cdef public set pins

    def __init__(self, netID):
        self.id = netID
        self.pins = set()
        self.cost = 0

    cpdef void update_ltrb(self) except *:
        i_pin = iter(self.pins)
        xp, yp = next(i_pin)
        cdef int x = xp, y = yp
        cdef int t = y, b = y
        cdef int l = x, r = x

        
        for x, y in i_pin:
            with nogil:
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