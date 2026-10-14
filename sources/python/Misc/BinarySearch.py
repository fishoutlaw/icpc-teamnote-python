"""원본: code/Misc/BinarySearch.cpp. 0-based.
Monotonic predicates; [lo,hi), O(log range) evaluations.
"""
def first_true(lo, hi, check):
    """정수 반열린 구간 [lo, hi)의 False...True 첫 True. 없으면 hi.

    check는 단조적이어야 한다. O(log(hi-lo+1))회 평가, 보조 공간 O(1).
    """
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def last_true(lo, hi, check):
    """정수 [lo, hi)의 True...False 마지막 True. 없으면 lo-1.

    O(log(hi-lo+1))회 평가, 보조 공간 O(1).
    """
    return first_true(lo, hi, lambda x: not check(x)) - 1
