from python.Misc.BinarySearch import first_true


def kth_multiplication_table(n, k):
    # n*n 곱셈표의 k번째 값. 1<=k<=n*n, O(n log n).
    def count_leq(x):
        return sum(min(n, x // i) for i in range(1, n + 1))
    # 개수가 k와 같아도 중단하지 않고, k 이상인 첫 위치를 찾는다.
    return first_true(1, n * n + 1, lambda x: count_leq(x) >= k)
