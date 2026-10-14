# 단조 조건의 경계를 구한다. 구간 [lo,hi), 조건 평가 O(log 범위).
def first_true(lo, hi, check):
    # [lo,hi)의 거짓→참 경계. 첫 참의 위치, 없으면 hi.
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def last_true(lo, hi, check):
    # [lo,hi)의 참→거짓 경계. 마지막 참의 위치, 없으면 lo-1.
    return first_true(lo, hi, lambda x: not check(x)) - 1
