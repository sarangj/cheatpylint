class Foo:

    # pylint: disable=too-many-arguments
    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        # pylint: enable=too-many-arguments

    # pylint: disable=too-many-arguments
    def modify(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        # pylint: enable=too-many-arguments


# pylint: disable=too-many-arguments
def modify(foo, a, b, c, d, e, f):
    foo.a = a
    foo.b = b
    foo.c = c
    foo.d = d
    foo.e = e
    foo.f = f
    # pylint: enable=too-many-arguments
