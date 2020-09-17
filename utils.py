from itertools import product
import operator as op
from functools import reduce


def argmax(*iterables, key=None):
    """ Maximizes the key function over iterables and returns
        the corresponding argument. """
    return max(product(*iterables), key=lambda args: key(*args))


def prod(iterable):
    """ Returns the product of the elements of an iterable. """
    return reduce(op.mul, iterable)


def get_mint(base):
    """ Returns a modular integer class for a given base. """

    class mint(int):
        base = base
        __slots__ = []

        def __new__(cls, val):
            return int.__new__(cls, val % cls.base)

        def __pow__(self, exponent):
            return mint(int.__pow__(self, exponent, self.base))

    def reduce(method):
        def inner(self, *args, **kwargs):
            return mint(method(self, *args, **kwargs))

        return inner

    for name in ["add", "radd", "sub", "rsub", "mul", "rmul", "neg"]:
        method = f"__{name}__"
        setattr(mint, method, reduce(getattr(int, method)))

    return mint

