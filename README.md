# ICPC Teamnote — Python / Python + C++

대회용 팀노트입니다. 원본의 49개 알고리즘·템플릿과 8개 분야, 수학 참고표·메모·체크리스트를 유지합니다. 설명은 README에 모으고 PDF는 표지 없이 목차부터 시작합니다. 알고리즘 본문은 경로·출처 줄과 긴 영어 설명을 없애고, 짧은 한글 주석과 코드로 구성합니다. 사용 조건·복잡도·반환값 등 필요한 설명은 주석에 남겼습니다.

| PDF | 분량 | 구성 |
|---|---:|---|
| **[Python판](icpc-teamnote-python.pdf)** | **19쪽** | 원본 49개 항목을 Python으로 변환 |
| **[Python + C++ 혼합판](icpc-teamnote-mixed.pdf)** | **22쪽** | Python 전용 15개 · C++ 전용 16개 · 양쪽 18개 |

두 PDF 모두 A4 가로 2단, **코드 8.5pt**, 최대 25쪽입니다. 혼합판은 쉬운 구현은 Python, 복잡하거나 성능에 민감한 구현은 C++, 상황에 따라 선택할 항목은 두 언어로 제공합니다. C++는 GNU C++17입니다.

**추가 판형: [혼합판 9pt PDF](sources/versions/icpc-teamnote-mixed-9pt.pdf) — 23쪽.** 기존 8.5pt 판은 그대로 유지합니다. 재생성은 `sources/`에서 `python scripts/build_mixed.py --font-size 9`, 검증은 `python scripts/verify_mixed_pdf.py --font-size 9`를 실행합니다.

## 세 버전 다운로드

각 ZIP은 별도 폴더에 풀어서 사용합니다. Python판과 혼합판에는 해당 PDF·소스·빌드 도구·테스트·출처가 포함됩니다.

| 버전 | 다운로드 | 설명 |
|---|---|---|
| 원본 C++ | [icpc-teamnote-cpp.zip](sources/versions/icpc-teamnote-cpp.zip) | 원본 코드, LaTeX, 스타일, PDF, README 보존 |
| Python | [icpc-teamnote-python.zip](sources/versions/icpc-teamnote-python.zip) | Python 전체 변환판과 재생성 도구 |
| Python + C++ | [icpc-teamnote-mixed.zip](sources/versions/icpc-teamnote-mixed.zip) | 혼합판, C++ 헤더 34개, Python 코드, 비교 검증 도구 |

원본 C++ PDF는 원본 상태를 보존하며 새 편집판의 25쪽 제한을 적용하지 않습니다. 원본 코드와 혼합판의 C++ 헤더는 별도 구현입니다.

## 저장소 구성

최상위 일반 파일은 두 PDF와 이 README입니다. 나머지는 `sources/`에 모았습니다. 숨김 Git 설정 파일은 저장소 관리용입니다.

```text
README.md
icpc-teamnote-python.pdf
icpc-teamnote-mixed.pdf
sources/
  versions/          # 버전별 ZIP 3개
  code/              # 수정하지 않은 원본 C++ 49개 파일
  python/            # Python 코드, 제출 템플릿, 참고 함수
  mixed/             # 혼합판 C++ 헤더, 언어 선택 목록, 검증 결과
  docs/              # 원본 문서, 변환 현황, 수학 참고
  scripts/           # PDF 빌드, 검증, ZIP 패키징
  tests/             # Python 테스트와 C++ 비교 테스트
  main.tex           # Python판 LaTeX
  mixed.tex          # 혼합판 LaTeX
  teamnote.sty
  requirements-pdf.txt
  ATTRIBUTION.md
```

## 코드 사용

Python은 3.10 이상과 표준 라이브러리를 사용합니다. 정점·배열 인덱스는 0부터, 기본 구간은 `[l, r)`입니다. 예외가 있는 함수는 파일 안의 한글 주석을 따릅니다. `sources/python/solve.py`는 제출 템플릿입니다.

PDF에서 긴 코드 행 앞의 `|`는 조판용 이어쓰기 표시입니다. 제출 코드는 소스 파일에서 필요한 import와 함수·클래스를 함께 복사하세요. C++는 `mixed/cpp/common.hpp`와 각 헤더가 참조하는 정의를 함께 사용합니다. `bits/stdc++.h`, `__int128`을 사용하므로 GNU C++17 환경이 필요합니다.

[변환 현황](sources/docs/PORTING.md) · [수학 참고와 정정](sources/docs/REFERENCE.md) · [혼합판 사용법과 언어별 차이](sources/mixed/README.md)

Python의 큰 정수·`Fraction`과 C++의 고정 폭 정수·실수는 특성이 다릅니다. C++ 도달 불가는 `tn::INF`, Python은 `math.inf`입니다. C++ 문자열은 바이트 단위이며 동일한 결과를 비교하려면 Python에서도 `bytes`를 사용합니다. 범위·정밀도·복잡도 조건은 각 소스와 혼합판 사용법에 적었습니다.

## PDF 재생성 및 검증

저장소에서는 먼저 `sources/`로 이동합니다. ZIP에서는 압축을 푼 폴더가 작업 디렉토리입니다.

```powershell
cd sources
python -m pip install -r requirements-pdf.txt
python -m unittest discover -s tests -v
python scripts/build_teamnote.py
python scripts/verify_pdf.py
python scripts/build_mixed.py
python scripts/verify_mixed_pdf.py
python scripts/verify_mixed.py
python scripts/package_versions.py
```

Python ZIP에서는 `build_teamnote.py`, `verify_pdf.py`와 Python 테스트를, 혼합판 ZIP에서는 `build_mixed.py`, `verify_mixed_pdf.py`, `verify_mixed.py`와 Python 테스트를 실행합니다. ZIP 재패키징은 저장소에서만 실행합니다. C++ 검증에는 PATH의 `g++`가 필요합니다.

PDF는 ReportLab으로 생성하며, 빌드 결과는 `sources/output/pdf/`와 저장소 최상위에 저장됩니다. ZIP에서는 `output/pdf/`와 압축 해제 폴더에 저장됩니다. 25쪽을 초과하면 빌드가 실패합니다. 글꼴은 Windows의 맑은 고딕·Consolas를 기본 사용하며, 다른 환경에서는 `TEAMNOTE_FONT`와 `TEAMNOTE_MONO`에 본문용 한글 지원 TTF와 코드용 TTF 경로를 지정합니다. 다른 글꼴에서는 페이지 수가 달라질 수 있습니다.

LaTeX 소스도 함께 생성하지만 제공 PDF는 ReportLab 결과입니다. LaTeX 컴파일은 검증하지 않았습니다. PDF 편집 후에는 자동 검사에 더해 Poppler 등으로 전 페이지를 렌더링하여 확인하세요.

## 검증 범위

- Python 22개 테스트 그룹: 경계 사례 및 무작위 입력을 기준 알고리즘과 비교.
- GNU g++ 15.2.0: C++ 헤더 34개 독립 컴파일 및 전체 링크, 고정 seed 비교 사례 1,195개 통과.
- PDF: 25쪽 제한, 전체 소스 내용 일치, 경로 표시 제거, 한글 텍스트, 페이지 경계 검사 및 전 페이지 시각 점검.

검증 환경은 Python 3.12.14입니다. 온라인 저지 제출 및 최대 입력 시간·메모리 벤치마크는 수행하지 않았습니다. 상세 결과는 [C++ 검증 기록](sources/mixed/validation.json)과 [혼합 PDF 검증 기록](sources/mixed/pdf-validation.json)에 있습니다.

## 원본과 출처

원본: [justiceHui/icpc-teamnote-for-newbie](https://github.com/justiceHui/icpc-teamnote-for-newbie), 기준 커밋 `73c55c4258f8a9c4417aa8537896d2de5d89fcae`.

[원본 README와 참고 자료](sources/docs/UPSTREAM_README.md) · [저자·출처 기록](sources/ATTRIBUTION.md)

원본 코드·문서와 저자 표기를 보존합니다. 원본에 없는 라이선스 권한을 새로 부여하지 않습니다. 각 코드의 저자와 참고 자료를 확인하세요.
