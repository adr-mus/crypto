import math
from collections import Counter
from functools import reduce
from itertools import count, product

import numpy as np

from numth.utils import prod

__all__ = ["lcm", "is_prime", "prime_factors", "factorize", "divisors", "no_divisors", "primes",
           "phi", "carmichael", "special", "cryptography", "modular", "utils"]


def lcm(*args):
    """ Returns the least common multiplicity of given numbers. """
    if len(args) == 2:
        return args[0] * args[1] // math.gcd(args[0], args[1])
    else:
        return reduce(lcm, args)


def is_prime(n):
    """ Checks whether n is prime. """
    n = abs(n)
    if n == 1 or (n % 2 == 0 and n != 2) or (n % 3 == 0 and n != 3):
        return False

    k = 5
    while k ** 2 <= n:
        if n % k == 0 or n % (k + 2) == 0:
            return False
        k += 6

    return True


def prime_factors(n):
    """ Generates the primes factors of n (with repetitions). """
    for k in [2, 3]:
        while n % k == 0:
            n //= k
            yield k
    k = 5
    while k ** 2 <= n:
        for r in [0, 2]:
            l = k + r
            while n % l == 0:
                n //= l
                yield l
        k += 6
    if n != 1:
        yield n


def factorize(n):
    """ If n = TT p_i^e_i, where p_i are pairwise different primes,
        returns a list of pairs (p_i, e_i). """
    return list(Counter(prime_factors(n)).items())


def divisors(n):
    """ Generates all divisors of n. """
    for i in range(1, round(n ** 0.5) + 1):
        if n % i == 0:
            yield i
            j = n // i
            if i != j:
                yield j


def no_divisors(*n):
    """ If an int is given, returns the number of its divisors.
        If two ints are given, returns the number of divisors 
        of n[0]^n[1] assuming n[0] is prime. """
    if len(n) == 2:
        return n[1] + 1
    elif len(n) == 1:
        return prod(no_divisors(_, e) for _, e in factorize(n[0]))
    else:
        raise ValueError("Invalid number of arguments.")
        

def primes(upper_bound):
    """ Generates primes up to a given upper bound inclusively
        using the sieve of Eratosthenes. """
    if upper_bound >= 2:
        yield 2
        sieve_bound = (upper_bound - 1) // 2
        sieve = [True for _ in range(sieve_bound)]
        crosslimit = (round(upper_bound ** 0.5) - 1) // 2
        for i in range(crosslimit):
            if sieve[i]:
                n = 2 * i + 3

                j = 3
                m = (n * j - 3) // 2
                while m < sieve_bound:
                    sieve[m] = False
                    j += 2
                    m = (n * j - 3) // 2

        for i in range(sieve_bound):
            if sieve[i]:
                yield 2 * i + 3


def phi(*n):
    """ Euler's totient function of n if given directly as an int or 
        n = n[0]^n[1] if two ints are given assuming n[0] is prime. """
    if len(n) == 1:
        n = n[0]
        if n == 1:
            return 1

        return prod(phi(p, e) for p, e in factorize(n))
    elif len(n) == 2:
        p, e = n
        return (p - 1) * p ** (e - 1) 
    else:
        raise ValueError("Invalid number of arguments.")


def carmichael(*n):
    """ Carmichael's reduced totient function of n if given directly 
        as an int or n = n[0]^n[1] if two ints are given assuming n[0] 
        is prime. """
    if len(n) == 2:
        p, e = n
        if p == 2 and e > 2:
            return 2 ** (e - 2)
        else:
            return phi(p, e)
    elif len(n) == 1:
        if n[0] == 1:
            return 1
        return lcm(*(carmichael(p, e) for p, e in factorize(n[0])))
    else:
        raise ValueError("Invalid number of arguments.")


import numth.special, numth.cryptography, numth.modular, numth.utils


