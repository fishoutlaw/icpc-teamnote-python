# 정수 점 (x,y)의 내적·외적·방향·거리 제곱. O(1).
# 실수 좌표를 쓰면 오차 허용 기준을 별도로 정해야 한다.


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def sub(a, b):
    return a[0] - b[0], a[1] - b[1]


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def ccw(a, b, c):
    value = orient(a, b, c)
    return (value > 0) - (value < 0)


def distance_squared(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
