# pylint: disable=too-many-instance-attributes
class Foo:

    def __init__(self, a, b, c, d, e, f, g, h):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h


    def modify(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
    # pylint: enable=too-many-instance-attributes


def modify(foo, a, b, c, d, e, f):
    foo.a = a
    foo.b = b
    foo.c = c
    foo.d = d
    foo.e = e
    foo.f = f
