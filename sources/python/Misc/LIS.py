"""원본: code/Misc/LIS.cpp. Strict LIS values, O(N log N), O(N) space.
For nondecreasing subsequence use bisect_right instead of bisect_left.
"""
from bisect import bisect_left


def lis(values):
    tails, ends, previous = [], [], [-1] * len(values)
    for i, value in enumerate(values):
        pos = bisect_left(tails, value)
        if pos:
            previous[i] = ends[pos - 1]
        if pos == len(tails):
            tails.append(value)
            ends.append(i)
        else:
            tails[pos], ends[pos] = value, i
    result = []
    i = ends[-1] if ends else -1
    while i != -1:
        result.append(values[i])
        i = previous[i]
    return result[::-1]
