"""원본: code/String/KMP.cpp. O(N+M) time, O(M) auxiliary space.
0-based match positions; empty pattern matches all N+1 boundaries.
"""


def prefix_function(pattern):
    fail = [0] * len(pattern)
    for i in range(1, len(pattern)):
        j = fail[i - 1]
        while j and pattern[i] != pattern[j]:
            j = fail[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        fail[i] = j
    return fail


def kmp(text, pattern):
    if not pattern:
        return list(range(len(text) + 1))
    fail, result, j = prefix_function(pattern), [], 0
    for i, char in enumerate(text):
        while j and char != pattern[j]:
            j = fail[j - 1]
        if char == pattern[j]:
            j += 1
        if j == len(pattern):
            result.append(i - j + 1)
            j = fail[j - 1]
    return result
