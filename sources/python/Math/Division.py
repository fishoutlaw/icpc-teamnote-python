"""원본: code/Math/Division.cpp. Integer division, signed operands.
gcd/lcm O(log max(|a|,|b|)) arithmetic operations. Divisor must be nonzero.
"""
from math import gcd, lcm


def floor_div(a, b):
    return a // b


def ceil_div(a, b):
    return -(-a // b)
