"""원본: code/String/SuffixArray.cpp. Doubling + counting sort, O(N log N).
Space O(N). Returns (sa,lcp); lcp[i]=LCP(sa[i-1],sa[i]), lcp[0]=0.
Unicode strings supported; all indices 0-based.
"""


def suffix_array(text):
    n = len(text)
    if not n:
        return [], []
    alphabet = {c: i + 1 for i, c in enumerate(sorted(set(text)))}
    rank = [alphabet[c] for c in text]
    sa, step = list(range(n)), 1

    def counting_sort(indices, keys, size):
        count = [0] * (size + 1)
        for i in indices:
            count[keys[i]] += 1
        for i in range(1, len(count)):
            count[i] += count[i - 1]
        result = [0] * len(indices)
        for i in reversed(indices):
            count[keys[i]] -= 1
            result[count[keys[i]]] = i
        return result

    while True:
        second = [rank[i + step] if i + step < n else 0 for i in range(n)]
        size = max(rank)
        sa = counting_sort(counting_sort(sa, second, size), rank, size)
        new, classes = [0] * n, 1
        new[sa[0]] = classes
        for a, b in zip(sa, sa[1:]):
            if (rank[a], second[a]) != (rank[b], second[b]):
                classes += 1
            new[b] = classes
        rank = new
        if classes == n:
            break
        step *= 2
    lcp, length = [0] * n, 0
    for i in range(n):
        pos = rank[i] - 1
        if pos == 0:
            length = 0
            continue
        j = sa[pos - 1]
        while i + length < n and j + length < n and text[i + length] == text[j + length]:
            length += 1
        lcp[pos] = length
        length = max(0, length - 1)
    return sa, lcp
