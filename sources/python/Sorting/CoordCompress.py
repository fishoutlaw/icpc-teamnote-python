"""원본: code/Sorting/CoordCompress.cpp. 0-based.
Coordinate compression O(N log N), space O(N).
"""
def coordinate_compress(values):
    """(0부터 시작하는 압축 좌표, 복원용 정렬 고유 값). O(N log N), 공간 O(N)."""
    unique = sorted(set(values))
    rank = {value: i for i, value in enumerate(unique)}
    return [rank[value] for value in values], unique
