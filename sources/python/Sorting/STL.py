"""원본: code/Sorting/STL.cpp. Sorted list required; 0-based positions.
bisect_left/right O(log N); inserting into a list is O(N).
"""
from bisect import bisect_left, bisect_right


def equal_range(values, x):
    """Half-open interval containing all occurrences of x."""
    return bisect_left(values, x), bisect_right(values, x)


def contains(values, x):
    i = bisect_left(values, x)
    return i < len(values) and values[i] == x


def nth_element(values, k):
    """In-place randomized quickselect. Expected O(N), worst O(N^2), O(1) space."""
    from random import randrange
    if not 0 <= k < len(values):
        raise IndexError(k)
    l, r = 0, len(values)
    while r - l > 1:
        pivot = values[randrange(l, r)]
        a = i = l
        b = r
        while i < b:
            if values[i] < pivot:
                values[a], values[i] = values[i], values[a]
                a += 1
                i += 1
            elif values[i] > pivot:
                b -= 1
                values[b], values[i] = values[i], values[b]
            else:
                i += 1
        if k < a:
            r = a
        elif k >= b:
            l = b
        else:
            break
    return values[k]
