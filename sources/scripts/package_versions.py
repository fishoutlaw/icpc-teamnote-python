"""Create three independent ZIP bundles from the repository sources."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'versions'
OUT.mkdir(exist_ok=True)


def files(relative):
    path = ROOT / relative
    assert path.exists(), path
    candidates = sorted(path.rglob('*')) if path.is_dir() else [path]
    return [p for p in candidates if p.is_file() and '__pycache__' not in p.parts
            and p.suffix not in ('.pyc', '.pyo')]


def bundle(name, groups, extra):
    entries = {}
    for group in groups:
        for path in files(group):
            entries[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    entries.update(extra)
    target = OUT / f'icpc-teamnote-{name}.zip'
    with ZipFile(target, 'w', compression=ZIP_DEFLATED) as archive:
        for path, data in sorted(entries.items()):
            info = ZipInfo(path, date_time=(2026, 10, 14, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    with ZipFile(target) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(entries)
    print(f'{target.name}: {len(entries)} files')


bundle('cpp', ['code', 'ATTRIBUTION.md'], {
    'README.md': (ROOT / 'docs/UPSTREAM_README.md').read_bytes(),
    **{p.name: p.read_bytes() for p in sorted((ROOT / 'docs/upstream').iterdir()) if p.is_file()},
})

common = ['python', 'code', 'docs', 'teamnote.sty', 'requirements-pdf.txt',
          'ATTRIBUTION.md', 'tests/test_algorithms.py', 'tests/test_full_teamnote.py',
          'scripts/pdf_checks.py']


def readme(title, commands, details):
    return (f'# ICPC {title} Teamnote\n\n'
            '압축을 푼 폴더에서 실행합니다. Python 3.10+가 필요합니다.\n\n'
            '```powershell\npython -m pip install -r requirements-pdf.txt\n'
            'python -m unittest discover -s tests -v\n' + commands + '\n```\n\n'
            + details + '\n\n'
            'PDF는 A4 가로 2단, 코드 8.5pt, 최대 25쪽입니다. '
            'Windows 맑은 고딕·Consolas를 사용합니다. 다른 환경에서는 '
            'TEAMNOTE_FONT와 TEAMNOTE_MONO에 TTF 경로를 지정하세요. '
            'PDF의 줄 이어쓰기 표시 | 는 소스 코드가 아닙니다.\n\n'
            '원본 49개 항목과 8개 분야를 유지합니다. code/와 docs/upstream/은 '
            '원본 출처 및 구조 확인용입니다. 출처: ATTRIBUTION.md 및 docs/UPSTREAM_README.md. '
            '온라인 저지 제출·최대 입력 벤치마크 및 LaTeX 컴파일은 검증하지 않았습니다.\n').encode('utf-8')


bundle('python', common + ['main.tex', 'scripts/build_teamnote.py', 'scripts/verify_pdf.py'], {
    'README.md': readme('Python', 'python scripts/build_teamnote.py\npython scripts/verify_pdf.py',
                       '19쪽. 알고리즘은 python/에 있습니다. 변환 차이는 docs/PORTING.md를 참조하세요.'),
    'icpc-teamnote-python.pdf': (ROOT / 'output/pdf/icpc-teamnote-python.pdf').read_bytes(),
})
bundle('mixed', common + ['mixed', 'mixed.tex', 'tests/mixed_runner.cpp',
                         'supplement', 'mixed-supplement.tex', 'mixed-supplement-9pt.tex',
                         'tests/test_supplement.py',
                         'scripts/supplement_manifest.py',
                         'scripts/build_mixed.py', 'scripts/mixed_manifest.py',
                         'scripts/verify_mixed.py', 'scripts/verify_mixed_pdf.py'], {
    'README.md': readme('Python + C++', 'python scripts/build_mixed.py\npython scripts/verify_mixed_pdf.py\npython scripts/verify_mixed.py',
                       '기본판 22쪽. Python 전용 15개, C++ 전용 16개, 양쪽 18개입니다. '
                       'versions/의 자료 추가판은 8.5pt 23쪽, 9pt 생성기 기준 24쪽입니다. '
                       '9pt 추가판은 별도 PDF 검증과 페이지 이미지 렌더링을 수행하지 않았습니다. '
                       '9pt 생성은 python scripts/build_mixed.py --supplement --font-size 9 --skip-validation입니다. '
                       'build_mixed.py와 '
                       'verify_mixed_pdf.py에 --supplement를 붙여 재생성·검증합니다. '
                       '추가 코드와 중복 제거 기록은 supplement/에 있습니다. '
                       'C++ 검증에는 PATH의 g++가 필요합니다. 사용 조건은 mixed/README.md를 참조하세요.'),
    'icpc-teamnote-mixed.pdf': (ROOT / 'output/pdf/icpc-teamnote-mixed.pdf').read_bytes(),
    'versions/icpc-teamnote-mixed-supplement.pdf': (ROOT / 'versions/icpc-teamnote-mixed-supplement.pdf').read_bytes(),
    'versions/icpc-teamnote-mixed-supplement-9pt.pdf': (ROOT / 'versions/icpc-teamnote-mixed-supplement-9pt.pdf').read_bytes(),
})
