# 정렬 리스트의 순위·k번째 조회 O(log N)·O(1), 삽입·삭제 O(N).
# 갱신이 많으면 좌표 압축과 펜윅 트리·세그먼트 트리를 사용한다.
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
    # 1인 비트 수가 같은, 현재 값보다 큰 최소 양의 정수.
    if x <= 0:
        raise ValueError('positive integer required')
    low = x & -x
    ripple = x + low
    return ripple | ((ripple ^ x) // low >> 2)


def digit_frequency(n, digit):
    # [1,n]에서 십진 숫자의 등장 횟수. 앞쪽 0 제외, O(log n).
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
