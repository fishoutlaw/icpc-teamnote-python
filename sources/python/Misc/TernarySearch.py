"""원본: code/Misc/TernarySearch.cpp.
Unimodal minimum, closed interval [lo,hi], smallest minimizer for integer search.
Requires strict decrease/increase outside the (possibly flat) minimum region.
Integer: O(log range) evaluations; real: O(iterations); space O(1).
"""


def ternary_integer(lo, hi, f):
    if lo > hi:
        raise ValueError('empty interval')
    while hi - lo > 3:
        a = lo + (hi - lo) // 3
        b = hi - (hi - lo) // 3
        if f(a) > f(b):
            lo = a + 1
        else:
            hi = b - 1
    return min(range(lo, hi + 1), key=f)


def ternary_real(lo, hi, f, iterations=100):
    for _ in range(iterations):
        a, b = (2 * lo + hi) / 3, (lo + 2 * hi) / 3
        if f(a) > f(b):
            lo = a
        else:
            hi = b
    return (lo + hi) / 2
