"""원본: code/Sorting/Compare.cpp. Stable sort O(N log N), space O(N).
key is evaluated once per item. For custom comparisons use cmp_to_key.
"""
from functools import cmp_to_key


def sort_points(points):
    """x ascending, then y ascending (same as original)."""
    return sorted(points, key=lambda p: (p[0], p[1]))


def sort_with_comparator(values, compare):
    """compare(a,b) must return negative / zero / positive consistently."""
    return sorted(values, key=cmp_to_key(compare))
