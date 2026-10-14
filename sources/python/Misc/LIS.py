# 엄격히 증가하는 최장 부분 수열 O(N log N).
# 같은 값도 허용하려면 bisect_left를 bisect_right로 바꾼다.
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
