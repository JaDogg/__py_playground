__author__ = 'bhathiyap'


class Foo(tuple):
    def __new__(cls, _, *args):
        return super(Foo, cls).__new__(cls, tuple(args))

    def __init__(self, label_string, *_):
        self.label = label_string


if __name__ == '__main__':
    foo = Foo("add", 2, "+", 3)
    print foo
    print foo.label
