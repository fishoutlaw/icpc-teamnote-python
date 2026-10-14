"""Approved language selection. No edits to the Python-only edition."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
CPP_ONLY = {
    'DataStructure/SegmentTreeLazy', 'DataStructure/PersistentSegmentTree',
    'DataStructure/ConvexHullTrick', 'Graph2/BCC', 'Graph2/Dinic', 'Graph2/MCMF',
    'Graph2/Hopcroft', 'Graph2/HLD', 'Math/LinearSieve',
    'Math/MillerRabin-PollardRho', 'Math/Convolution', 'String/Hashing',
    'String/SuffixArray', 'Geometry/ConvexHull', 'Geometry/Calipers',
    'Geometry/PointInConvexPolygon',
}
BOTH = {
    'Graph1/Dijkstra', 'Graph1/Floyd', 'Graph1/Bellman', 'Graph1/Kruskal',
    'DataStructure/SegmentTree', 'Graph2/SCC', 'Graph2/LCA',
    'Math/ChineseRemainderTheorem', 'Math/Matrix', 'String/KMP', 'String/Z',
    'String/Manacher', 'Geometry/Template', 'Geometry/PolarSort',
    'Geometry/SegmentIntersection', 'Geometry/PointInPolygon',
    'Misc/LIS', 'Misc/FastIO',
}


def inventory():
    events = json.loads((ROOT / 'docs/manifest.json').read_text(encoding='utf-8'))
    for event in events:
        if 'path' not in event:
            continue
        key = Path(event['original']).relative_to('code').with_suffix('').as_posix()
        event['key'] = key
        event['languages'] = ['C++'] if key in CPP_ONLY else ['Python', 'C++'] if key in BOTH else ['Python']
        event['sources'] = {}
        if 'Python' in event['languages']:
            event['sources']['Python'] = event['path']
        if 'C++' in event['languages']:
            event['sources']['C++'] = f'mixed/cpp/{key}.hpp'
        for path in event['sources'].values():
            assert (ROOT / path).is_file(), path
    assert sum('key' in e for e in events) == 49
    actual = {e['key'] for e in events if 'key' in e}
    assert (CPP_ONLY | BOTH) <= actual and not CPP_ONLY & BOTH
    return events


if __name__ == '__main__':
    events = inventory()
    (ROOT / 'mixed/manifest.json').write_text(json.dumps(events, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'49 entries: {49-len(CPP_ONLY)-len(BOTH)} Python, {len(CPP_ONLY)} C++, {len(BOTH)} dual')
