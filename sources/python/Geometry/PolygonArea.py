# 경계 순서로 주어진 단순 다각형의 넓이 두 배를 정수로 구한다. O(N).


def polygon_area2(points):
    return abs(sum(points[i][0] * points[(i + 1) % len(points)][1]
                   - points[i][1] * points[(i + 1) % len(points)][0]
                   for i in range(len(points))))
