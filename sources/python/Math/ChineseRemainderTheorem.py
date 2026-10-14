"""원본: code/Math/ChineseRemainderTheorem.cpp. General CRT, positive moduli.
Returns (residue,lcm), or None if inconsistent. Empty input -> (0,1).
O(K log M) modular arithmetic steps, O(1) additional integers.
"""
from math import gcd


def crt(congruences):
    a, m = 0, 1
    for b, n in congruences:
        if n <= 0:
            raise ValueError('positive modulus required')
        g = gcd(m, n)
        if (b - a) % g:
            return None
        reduced = n // g
        t = ((b - a) // g * pow(m // g, -1, reduced)) % reduced
        a += m * t
        m *= reduced
        a %= m
    return a, m
