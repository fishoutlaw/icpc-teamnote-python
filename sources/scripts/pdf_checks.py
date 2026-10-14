"""Verify printed source contents without printing source paths in the PDF."""
import re


def compact(text):
    # The renderer inserts whitespace and a vertical bar at wrapped code lines.
    return re.sub(r'\s+', '', text).replace('|', '')


def verify_sources(reader, root, paths):
    bodies = []
    for number, page in enumerate(reader.pages, 1):
        lines = page.extract_text().splitlines()
        assert lines[0].startswith('ICPC'), (number, lines[:3])
        assert lines[2] == str(number), (number, lines[:3])
        bodies.append('\n'.join(lines[3:]))
    printed = compact('\n'.join(bodies))
    for path in paths:
        source = (root / path).read_text(encoding='utf-8')
        assert compact(source) in printed, f'Missing or changed printed source: {path}'
    for unwanted in ('python/', 'mixed/cpp/', 'code/', 'docs/upstream/', 'Based on code', '원본:'):
        assert unwanted not in printed, f'Unexpected source label: {unwanted}'
    return printed
