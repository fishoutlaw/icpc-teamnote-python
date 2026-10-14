# 중복을 제거하고 정렬한 값에 0부터 번호를 붙인다.
def coordinate_compress(values):
    # (0부터 시작하는 압축 좌표, 복원용 정렬 고유 값). O(N log N), 공간 O(N).
    unique = sorted(set(values))
    rank = {value: i for i, value in enumerate(unique)}
    return [rank[value] for value in values], unique
