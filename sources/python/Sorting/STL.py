# 정렬 배열의 경계 탐색 O(log N). 리스트 삽입은 O(N).
from bisect import bisect_left, bisect_right


def equal_range(values, x):
    # 정렬 배열에서 x가 나타나는 구간 [왼쪽, 오른쪽)을 구한다.
    return bisect_left(values, x), bisect_right(values, x)


def contains(values, x):
    i = bisect_left(values, x)
    return i < len(values) and values[i] == x


def nth_element(values, k):
    # 배열을 직접 바꾸어 k번째 값을 선택한다. 기대 O(N), 최악 O(N^2).
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
