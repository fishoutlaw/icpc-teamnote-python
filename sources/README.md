# 소스와 제작 도구

[배포 PDF·ZIP 및 사용법](../README.md)을 참조하세요.

이 폴더에서 Python 테스트와 `scripts/`의 빌드·검증·패키징 명령을 실행합니다. 코드 경로는 이 폴더를 기준으로 합니다.

- `code/`, `docs/upstream/`: 원본 C++ 코드와 문서.
- `python/`: 전체 Python 변환판.
- `mixed/`: 혼합판 C++ 헤더와 언어 선택 목록.
- `supplement/`: 8.5pt 자료 추가판의 Python 참조·추가 알고리즘·제공 원문.
- `versions/`: 원본 C++, Python, 혼합판의 독립 배포 ZIP.
- `output/`, `tmp/`: 자동 생성되는 중간 산출물로 Git에서 제외합니다.

최상위 PDF 두 파일은 빌드 스크립트가 갱신합니다. 소스나 PDF를 수정했다면 검증 후 `python scripts/package_versions.py`로 ZIP도 갱신하세요.
