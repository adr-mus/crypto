import math


def fibonacci(upper_bound=math.inf):
    """ Generates the Fibonacci numbers up to a given upper bound.
        If none is given, generates them indefinitely. """
    if upper_bound > 1:
        a, b = 1, 1
        while a < upper_bound:
            yield a
            a, b = b, a + b


def expand_cf(int_part, expansion):
    """ Expands a continued fraction based on its integer part and its 
        truncated expansion. Returns a pair (numerator, denominator). """
    num, den = 0, 1
    for n in reversed(expansion):
        num += n * den
        num, den = den, num
    num += int_part * den
    gcd = math.gcd(num, den)

    return num // gcd, den // gcd


def convergents(r, n=math.inf):
    """ Generates the sequence of convergents for a given positive number r
        (pairs of form (numerator, denominator)).
        If n is given, generates n first convergents of n.
        Otherwise generates convergents indefinitely. """
    int_part = math.floor(r)
    curr_fr_part = r - int_part
    expansion = []
    k = 1
    while k <= n:
        yield expand_cf(int_part, expansion)
        k += 1

        t = 1 / curr_fr_part
        curr_int_part = math.floor(t)
        expansion.append(curr_int_part)
        curr_fr_part = t - curr_int_part


def solve_pell(D):
    """ Finds the minimal solution (x0, y0) of the equation x^2 - D*y^2 = 1
        using the Chakravala method. """
    b = 1
    a = math.ceil(math.sqrt(D))
    k = a ** 2 - D
    if k == 0:  # D is a square number => no solutions
        return
    while k != 1:
        nums = (
            m for m in range(math.floor(math.sqrt(2 * D)) + 1) if (a + b * m) % k == 0
        )
        m = min(nums, key=lambda m: abs(m ** 2 - D))
        a, b, k = (a * m + D * b) // abs(k), (a + b * m) // abs(k), (m ** 2 - D) // k

    return a, b
