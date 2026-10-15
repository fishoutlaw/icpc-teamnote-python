import sys, math
from collections import Counter, defaultdict
from itertools import accumulate, combinations, permutations
input = sys.stdin.readline

a = list(map(int, input().split()))  # 정수 배열 입력
x, y = map(int, input().split())  # 언패킹 (map은 iterator)
s = input().strip()  # 양끝 공백 제거 (줄바꿈 포함)
print(*a)  # 공백 구분 출력
print(*a, sep='\n')  # 줄바꿈 출력
print(' '.join(map(str, a)))  # str 변환 후 합치기
for i, x in enumerate(a): ...  # (인덱스, 값)
for x, y in zip(A, B): ...  # 짧은 쪽 길이까지만
q, r = divmod(x, y)  # 몫, 나머지 (y != 0)
sum(x > 0 for x in a)  # 조건 만족 개수
any(x > 0 for x in a)  # 하나라도 True
all(x > 0 for x in a)  # 모두 True (빈 배열은 True)
min(a, default=-1)  # 빈 iterable 허용
max(a, key=lambda x: x[1])  # 두 번째 요소 기준 최대
a.index(x)  # 첫 인덱스, 없으면 ValueError
a.count(x)  # O(N)
a.append(x)  # 끝 삽입: 분할 상환 O(1)
a.insert(i, x)  # 중간 삽입: O(N)
a.pop()  # 끝 삭제: O(1)
a.pop(0)  # 앞 삭제: O(N) -> deque 사용
b = a[::-1]  # 역순 사본 O(N)
a.reverse()  # 제자리 뒤집기, None 반환
b = a[:]  # 얕은 복사 (내부 객체 공유)
b = a  # 복사 X (같은 객체 참조)
grid = [[0] * m for _ in range(n)]  # 2차원 배열: 행 각각 생성
grid = [[0] * m] * n  # 금지! 모든 행이 같은 객체
st = set(a)  # 중복 제거, 순서 보장 X
st.add(x); st.discard(x)  # discard는 없어도 오류 X
st.remove(x)  # 없으면 KeyError
x in st; x in dictionary  # 평균 O(1)
x in a  # 리스트 탐색 O(N)
Counter(a)[x]  # 등장 횟수
defaultdict(int)['missing']  # 기본값 0
list(accumulate(a))  # 누적합
list(combinations(a, 2))  # 조합 (생성량 주의)
list(permutations(a, 2))  # 순열 (생성량 주의)
ord('a'); chr(97)  # 문자 <-> 코드포인트
math.isqrt(n)  # floor(sqrt(n)), 정수 정확
math.ceil(x); math.floor(x)  # 올림 / 내림
len(str(abs(n)))  # 자릿수 (n=0이면 1)
list(map(int, str(n)))  # 양의 정수 자릿수 추출
