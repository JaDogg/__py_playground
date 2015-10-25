"""
While learning about numpy arrays, I'm writing my own imitation to get
the idea of them.
"""

# The 1d case, to warm ourselves up.

## p = Array1d([3,1,4,1,5,9,2,6,5,3,5,8,9,7,9])
## p.contents()
#. [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9]
## len(p)
#. 15
## q = Array1d(p, 1, 12)
## q.contents()
#. [1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8]
## len(q)
#. 11
## r = Array1d(q, 2, 10, 2)
## r.contents()
#. [1, 9, 6, 3]
## len(r)
#. 4
## s = Array1d(r, 0, 100, 3)
## s.contents()
#. [1, 3]
## len(s)
#. 2

## s[0], s[1]
#. (1, 3)
## s[2]
#. Traceback (most recent call last):
#.   File "arrayviews.py", line 80, in __getitem__
#.     if not (self.start <= i < self.end): raise IndexError("list index out of range")
#. IndexError: list index out of range

## dir([])
#. ['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']

class Array1d:
    """A view into a possibly-shared underlying mutable 1d array,
    with a start, end, and stride."""
    # TODO: negative end
    # TODO: negative stride

    def __init__(self, elements, start=None, end=None, stride=None):
        if start is None:  start = 0
        if end is None:    end = len(elements)
        if stride is None: stride = 1
        if isinstance(elements, list):
            self.elements = elements
            self.start    = start
            self.end      = end
            self.stride   = stride
        elif isinstance(elements, Array1d):
            self.elements = elements.elements
            self.start    = elements.start + start * elements.stride
            self.end      = min(end * elements.stride, elements.end)
            self.stride   = stride * elements.stride
        else:
            assert False
        self.self_check()

    def self_check(self):
        assert isinstance(self.elements, list)
        assert isinstance(self.start, int)  and 0 <= self.start
        assert isinstance(self.end, int)    and 0 <= self.end
        assert isinstance(self.stride, int) and 0 < self.stride

    def contents(self):
        return self.elements[self.start : self.end : self.stride]

    def __len__(self):
        result = (self.end + self.stride - 1 - self.start) // self.stride
        assert result == len(self.contents())
        return result

    def __getitem__(self, key):
        if not isinstance(key, int): raise TypeError("list indices must be integers")
        i = self.start + self.stride * key
        if not (self.start <= i < self.end): raise IndexError("list index out of range")
        return self.elements[i]
