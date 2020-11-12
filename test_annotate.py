import annotate


def test_disable_too_many_args(tmp_path):
    src_file = tmp_path / 'src.py'
    src_file.write_text("""
def f(x1, x2, x3, x4, x5, x6):
    pass
    """,
    )
    annotate.run_annotater('too-many-arguments', str(src_file))
    assert src_file.read_text() == """
# pylint: disable=too-many-arguments
def f(x1, x2, x3, x4, x5, x6):
    pass
    # pylint: enable=too-many-arguments
    """


def test_disable_too_many_instance_attributes(tmp_path):
    src_file = tmp_path / 'src.py'
    src_file.write_text("""
class Foo:

    # pylint: disable=too-many-arguments
    def __init__(self, a, b, c, d, e, f, g, h):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        # pylint: enable=too-many-arguments
    """,
    )
    annotate.run_annotater('too-many-instance-attributes', str(src_file))
    assert src_file.read_text() == """
# pylint: disable=too-many-instance-attributes
class Foo:

    # pylint: disable=too-many-arguments
    def __init__(self, a, b, c, d, e, f, g, h):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f
        self.g = g
        self.h = h
        # pylint: enable=too-many-arguments
    # pylint: enable=too-many-instance-attributes
    """
