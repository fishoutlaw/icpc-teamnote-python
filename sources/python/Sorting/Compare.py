# 안정 정렬 O(N log N). 같은 키의 원래 순서를 유지한다.
from functools import cmp_to_key


def sort_points(points):
    # x 오름차순, 같으면 y 오름차순.
    return sorted(points, key=lambda p: (p[0], p[1]))


def sort_with_comparator(values, compare):
    # 비교 함수는 a<b, a=b, a>b에 각각 음수·0·양수를 반환한다.
    return sorted(values, key=cmp_to_key(compare))
