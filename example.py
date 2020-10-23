class Foo:

    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def modify(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f


def modify(foo, a, b, c, d, e, f):
    foo.a = a
    foo.b = b
    foo.c = c
    foo.d = d
    foo.e = e
    foo.f = f
