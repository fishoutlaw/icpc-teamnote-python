"""원본: code/Geometry/Template.cpp. Points are (x,y) integer tuples.
Exact orientation, dot, cross, squared distance: O(1) integer operations.
Floating point coordinates require an application-specific tolerance policy.
"""


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
