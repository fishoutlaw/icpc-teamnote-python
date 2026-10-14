"""Check budget, full source inventory, layout bounds and Python-edition preservation."""
from pathlib import Path
import json
import argparse
from pypdf import PdfReader
import pdfplumber
from pdf_checks import verify_sources

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--font-size', type=float, choices=(8.5, 9.0), default=8.5)
args = parser.parse_args()
suffix = '-9pt' if args.font_size == 9 else ''
path = ROOT / f'output/pdf/icpc-teamnote-mixed{suffix}.pdf'
reader = PdfReader(path)
assert len(reader.pages) <= 25
text = '\n'.join(page.extract_text() for page in reader.pages)
assert '\ufffd' not in text
assert '문제 풀이 체크리스트' in text
assert 'C++17' in text and '[PY/C++]' in text
events = json.loads((ROOT / 'mixed/manifest.json').read_text(encoding='utf-8'))
paths = [source for event in events for source in event.get('sources', {}).values()]
count = len(paths)
assert count == 67
verify_sources(reader, ROOT, paths + ['mixed/cpp/common.hpp', 'python/Misc/Reference.py'])
assert 'common.hpp' in (ROOT / f'mixed{suffix}.tex').read_text(encoding='utf-8')
with pdfplumber.open(path) as doc:
    code_chars = [c for page in doc.pages for c in page.chars if 'Consolas' in c['fontname']]
    assert code_chars and all(abs(c['size'] - args.font_size) < 0.01 for c in code_chars)
    for number, page in enumerate(doc.pages, 1):
        for char in page.chars:
            assert 20 <= char['x0'] <= char['x1'] <= page.width - 20, (number, char)
            assert 5 <= char['top'] <= char['bottom'] <= page.height - 5, (number, char)
publish = ROOT / 'versions' if suffix else (ROOT.parent if ROOT.name == 'sources' else ROOT)
assert (publish / path.name).read_bytes() == path.read_bytes()
report = {'pages':len(reader.pages), 'page_limit':25, 'algorithm_entries':49,
          'language_snippets':count, 'code_font_pt':args.font_size,
          'source_inventory':'passed', 'page_bounds':'passed',
          'published_copy_matches':True}
(ROOT / f'mixed/pdf-validation{suffix}.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, indent=2))
