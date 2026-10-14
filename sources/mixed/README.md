# ICPC C++ / Python 혼합 팀노트

[PDF와 배포 안내](../README.md)

대회에서 구현하기 쉬운 항목은 Python, 복잡하거나 성능에 민감한 항목은 C++, 입력 규모에 따라 선택이 달라지는 항목은 두 언어로 수록합니다. 원본 49개 항목은 모두 유지합니다.

- Python 전용 15개, C++ 전용 16개, 두 언어 18개: 총 67개 언어별 코드 조각
- 원본 순서의 8개 분야, 수학 참고표·메모·체크리스트 유지
- 표지 없이 목차부터 시작, A4 가로 2단, 코드 8.5pt, **22쪽 / 최대 25쪽**
- 9pt 별도 판은 23쪽. 알고리즘 본문은 경로 표시 없이 짧은 한글 주석과 코드로 구성
- Python판과 원본 C++를 별도 파일로 제공

## 파일과 사용법

- `cpp/`: 혼합판에 수록하는 C++17 헤더 34개. 원본 `code/`와 같은 분야별 디렉토리를 사용합니다.
- `cpp/common.hpp`: 공통 include, `tn` 네임스페이스, 정수형과 INF 정의.
- `../python/`: Python판의 검증된 파일을 재사용합니다. 혼합판 수록 여부는 manifest로 관리합니다.
- `manifest.json`: 49개 항목의 제목·원본·선택 언어·코드 경로.
- `../mixed.tex`: 혼합판 LaTeX 소스. PDF는 ReportLab으로 렌더링합니다.
- `validation.json`: 컴파일러와 C++/Python 비교 검증 결과.
- `pdf-validation.json`: 페이지 수, 전체 소스 내용 일치, 페이지 경계 검사 결과.

C++ 헤더는 각각 필요한 의존성을 include합니다. PDF에서 복사할 때도 공통 정의와 참조하는 헤더의 정의를 함께 가져와야 합니다. 기하의 공통 연산은 `Geometry/Template.hpp`에 모아 중복을 줄였습니다.

```cpp
#include "mixed/cpp/Graph1/Dijkstra.hpp"
int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::vector<std::vector<std::pair<int, long long>>> g(3);
    g[0].push_back({1, 5});
    g[1].push_back({2, 7});
    auto [distance, parent] = tn::dijkstra(g, 0);
    std::cout << distance[2] << '\n';
}
```

`sources/`(ZIP에서는 압축 해제한 폴더)에서 GNU C++17로 컴파일합니다. `bits/stdc++.h`와 `__int128`을 사용하므로 MSVC 전용 환경은 대상이 아닙니다. PDF의 이어쓰기 표시 `|`는 소스 코드가 아닙니다. 가능하면 해당 파일에서 복사하세요.

## 통일한 규약과 언어 차이

- 정점·배열은 0-based, 구간은 기본 `[l,r)`. 삼분 탐색처럼 다른 구간을 쓰는 함수는 개별 설명을 따릅니다.
- C++ 거리 배열의 도달 불가는 `tn::INF`, Python은 `math.inf`입니다. 실패 반환은 C++ `nullopt`, Python `None`입니다. 경로 복원은 도달 불가 시 빈 배열을 반환합니다.
- C++ 합·거리·유량·비용의 중간 결과는 `(-INF, INF)` 안에 있어야 합니다. C++는 자동으로 큰 정수가 되지 않습니다.
- C++ 문자열 코드는 바이트 단위입니다. Python에서도 `bytes`를 넣으면 동일한 인덱스로 비교할 수 있습니다. Python `str`은 유니코드 문자 단위입니다.
- 행렬은 Python 기본값이 `Fraction` 정확 연산이고, C++ `RealOps`는 `long double` 근사 연산입니다. 소수 모듈러 모드(Python `mod`, C++ `ModOps`)는 양쪽 모두 정확합니다. C++ `RealOps.eps`는 입력 스케일에 맞춰 조절합니다.
- 선분 교차의 고유 교점은 Python `Fraction`, C++ `(xnum/den, ynum/den)` 정수 비율입니다. C++의 `kind`는 0:없음, 1:고유 교점, -1:겹치는 구간으로 같습니다. 실수가 필요하면 `long double(xnum)/den`으로 변환합니다.
- C++ 기하는 좌표 절댓값 10^9 이하를 전제로 `__int128` 외적을 사용합니다. 더 큰 좌표는 곱셈 범위를 다시 확인해야 합니다.
- 동적 직선 집합은 Li Chao 트리를 사용하며 정수 x 범위를 생성자에 지정합니다. C++ CHT의 기울기·절편·x는 절댓값 10^9 이하입니다.
- C++ 모듈러 합성곱은 임의의 양의 31-bit 모듈러스, 변환 길이 최대 2^24에서 NTT/CRT를 사용합니다. 지원 길이·복원 상한을 넘으면 예외를 냅니다. 기존 Python판의 O(NM) fallback과 이 부분은 다릅니다. 실수 FFT는 양쪽 모두 반올림 오차가 가능합니다.
- Miller–Rabin은 uint64 범위에서 확정 판별합니다. MCMF는 도달 가능한 음수 비용 사이클을 명시적으로 거부합니다.

## 검증

GNU g++ 15.2.0, `-std=c++17 -O2`로 헤더 34개를 각각 독립 컴파일하고 전체를 함께 링크했습니다. 고정 seed의 **1,195개 비교 사례**를 통과했습니다. 세그먼트 트리 등 한 사례 내부에서 여러 연산을 수행하므로 실제 비교한 질의 수는 더 많습니다.

비교 대상은 기존 Python 구현이며, 이 Python 구현은 별도의 22개 테스트에서 완전 탐색·기준 알고리즘과 비교합니다. C++ 테스트에는 최소 컷·최소 정점 커버 불변식, 역행렬 곱셈, 3,000정점 체인, uint64 경계, 64KiB 입력 버퍼 경계도 포함합니다.

온라인 저지 제출과 최대 입력의 시간·메모리 벤치마크는 아직 수행하지 않았습니다. 원본의 오류를 그대로 복사하지 않고 경계 처리를 보완했으며, 원본 파일과 Git 이력은 보존합니다. 출처는 [ATTRIBUTION.md](../ATTRIBUTION.md)를 참조하세요.

저장소에서는 먼저 `cd sources`를 실행합니다.

```powershell
python -m unittest discover -s tests -v
python scripts/verify_mixed.py
python scripts/build_mixed.py
python scripts/verify_mixed_pdf.py
```

PDF 빌드에는 ReportLab과 pypdf, PDF 경계 검사에는 pdfplumber가 필요합니다. 글꼴은 기존 PDF 빌드와 동일하게 `TEAMNOTE_FONT`·`TEAMNOTE_MONO`로 지정할 수 있습니다. LaTeX 소스는 생성했지만 이 환경에서 TeX 컴파일 자체는 검증하지 않았습니다.

혼합판 빌드는 25쪽을 초과하면 실패합니다. PDF를 변경한 후에는 Poppler로 전 페이지를 PNG로 렌더링해 육안 검토도 수행합니다. GitHub에 push하는 작업은 포함하지 않습니다.
