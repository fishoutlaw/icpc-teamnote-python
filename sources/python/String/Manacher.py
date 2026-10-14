# 구분자를 넣은 2N+1개 중심의 팰린드롬 반지름. O(N).
# 반지름은 원문 팰린드롬 길이이며 구분자는 입력 문자와 충돌하지 않는다.


def manacher(text):
    separator = object()
    values = [separator]
    for char in text:
        values.extend((char, separator))
    radius = [0] * len(values)
    center = right = 0
    for i in range(len(values)):
        if i < right:
            radius[i] = min(right - i, radius[2 * center - i])
        while (i - radius[i] > 0 and i + radius[i] + 1 < len(values)
               and values[i - radius[i] - 1] == values[i + radius[i] + 1]):
            radius[i] += 1
        if i + radius[i] > right:
            center, right = i, i + radius[i]
    return radius
