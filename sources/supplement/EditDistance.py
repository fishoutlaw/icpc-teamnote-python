def edit_distance(a, b):
    # 삽입·삭제·교체 비용 각 1. 시간·공간 O(len(a)*len(b)).
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i  # 빈 문자열로 만드는 삭제 비용
    for j in range(m + 1):
        dp[0][j] = j  # 빈 문자열에서 시작하는 삽입 비용
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = min(dp[i-1][j] + 1,
                           dp[i][j-1] + 1,
                           dp[i-1][j-1] + (a[i-1] != b[j-1]))
    return dp[n][m]

# DP 점검: 상태 의미 → 초기값 → 점화식 → 순회 순서 → 답 위치.
# 최댓값의 불가능 상태는 -INF, 경우의 수는 모듈러 적용 확인.
# 1차원 압축 시 이전 행과 현재 행의 값을 섞지 않는다.
