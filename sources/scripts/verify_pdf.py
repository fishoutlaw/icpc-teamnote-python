"""Optional PDF QA (pypdf/pdfplumber): bounds, glyph text, code inventory.
Also render with: pdftoppm -scale-to 1600 -png main.pdf tmp/pdfs/page
Visual inspection of those pages is required after layout changes.
"""
from pathlib import Path
import json
from pypdf import PdfReader
import pdfplumber

root = Path(__file__).resolve().parents[1]
pdf = root / 'output/pdf/icpc-teamnote-python.pdf'
reader = PdfReader(pdf)
assert len(reader.pages) <= 25
text = '\n'.join(page.extract_text() for page in reader.pages)
assert '\ufffd' not in text
assert '문제 풀이 체크리스트' in text
manifest = json.loads((root / 'docs/manifest.json').read_text(encoding='utf-8'))
for item in manifest:
    if 'path' in item:
        assert item['path'] in text, item['path']
with pdfplumber.open(pdf) as document:
    for number, page in enumerate(document.pages, 1):
        for char in page.chars:
            assert 20 <= char['x0'] <= char['x1'] <= page.width - 20, (number, char)
            assert 5 <= char['top'] <= char['bottom'] <= page.height - 5, (number, char)
publish = root.parent if root.name == 'sources' else root
assert (publish / 'icpc-teamnote-python.pdf').read_bytes() == pdf.read_bytes()
print(f'{len(reader.pages)} pages; all 49 code paths, Korean text and page bounds verified.')
