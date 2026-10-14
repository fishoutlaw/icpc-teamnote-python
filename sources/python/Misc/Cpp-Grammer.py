"""원본: code/Misc/Cpp-Grammer.cpp. Python equivalents, no GCC extensions.
random.randint(lo,hi), random.random(), random.Random(seed) for reproducibility.
bits: x.bit_count(), x.bit_length(), x & -x. x must be nonnegative.
Rope replacement: collect fragments then ''.join(parts); slicing copies O(k).
OrderedSet below uses stdlib sorted list: rank/select O(log N)/O(1),
insert/delete O(N). Use compressed Fenwick/segment tree for many updates.
"""
from bisect import bisect_left


class OrderedSet:
    def __init__(self, values=()):
        self.values = sorted(set(values))

    def add(self, value):
        i = bisect_left(self.values, value)
        if i == len(self.values) or self.values[i] != value:
            self.values.insert(i, value)

    def discard(self, value):
        i = bisect_left(self.values, value)
        if i < len(self.values) and self.values[i] == value:
            self.values.pop(i)

    def order_of_key(self, value):
        return bisect_left(self.values, value)

    def find_by_order(self, index):
        return self.values[index]


def trailing_zeros(x):
    if x <= 0:
        raise ValueError('positive integer required')
    return (x & -x).bit_length() - 1


def leading_zeros(x, width=64):
    if not 0 <= x < 1 << width:
        raise ValueError('value outside unsigned width')
    return width - x.bit_length()


def next_same_popcount(x):
    """Smallest larger positive integer with same number of set bits."""
    if x <= 0:
        raise ValueError('positive integer required')
    low = x & -x
    ripple = x + low
    return ripple | ((ripple ^ x) // low >> 2)


def digit_frequency(n, digit):
    """Count decimal digit in [1,n], no leading zeros. O(log n)."""
    if not 0 <= digit <= 9:
        raise ValueError('invalid digit')
    answer, place = 0, 1
    while place <= n:
        high, current, low = n // (place * 10), n // place % 10, n % place
        if digit:
            answer += high * place
        elif high:
            answer += (high - 1) * place
        if digit or high:
            if current > digit:
                answer += place
            elif current == digit:
                answer += low + 1
        place *= 10
    return answer
