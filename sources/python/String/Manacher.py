"""원본: code/String/Manacher.cpp. O(N) time/space.
Returns 2*N+1 radii with separators; radius equals original palindrome length.
Separator is a unique object, so literal '#' in input is safe.
"""


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
