"""Compile C++17, compare all 34 C++ entries against tested Python versions.
Fixed seed; results in mixed/validation.json. Requires g++ on PATH.
Run Python unit tests separately for independent brute-force checks.
"""
import importlib.util
from pathlib import Path
import collections
import json
import math
import os
import random
import shutil
import subprocess
from fractions import Fraction
from mixed_manifest import inventory, ROOT

TMP = ROOT / 'tmp/mixed'
TMP.mkdir(parents=True, exist_ok=True)
compiler = shutil.which('g++')
if not compiler:
    raise RuntimeError('GNU C++ compiler g++ not found')
flags = ['-std=c++17', '-O2', '-Wall', '-Wextra', '-Wno-misleading-indentation']
runner = TMP / ('runner.exe' if os.name == 'nt' else 'runner')
print('Compiling runner and checking standalone headers...', flush=True)
subprocess.run([compiler, *flags, str(ROOT / 'tests/mixed_runner.cpp'), '-o', str(runner)], check=True)
events = inventory()
headers = [e['sources']['C++'] for e in events if 'C++' in e.get('languages', [])]
translation_units = []
for index, header in enumerate(headers):
    file = TMP / f'header_{index}.cpp'
    file.write_text('#include "' + (ROOT / header).as_posix() + '"\n', encoding='utf-8')
    translation_units.append(str(file))
subprocess.run([compiler, '-std=c++17', '-fsyntax-only', *translation_units], check=True)


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('/', '_'), ROOT / 'python' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def flat(values):
    return [x for row in values for x in row]


def vec(values):
    return [len(values), *values]


def dist(values):
    return ['X' if x == math.inf else x for x in values]


rng = random.Random(20261014)
cases = []


def add(op, args, expected):
    cases.append((op, ' '.join(map(str, [op, *args])), ' '.join(map(str, expected))))


print('Preparing deterministic differential cases...', flush=True)
dj, fw, bf = load('Graph1/Dijkstra'), load('Graph1/Floyd'), load('Graph1/Bellman')
mst = load('Graph1/Kruskal')
for _ in range(55):
    n = rng.randrange(1, 10)
    edges = [(u, v, rng.randrange(15)) for u in range(n) for v in range(n) if rng.random() < .23]
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    s, t = rng.randrange(n), rng.randrange(n)
    d, p = dj.dijkstra(graph, s)
    add('dist', [n, len(edges), s, t, *flat(edges)], dist(d) + vec(dj.restore_path(p, s, t)) + dist(flat(fw.floyd_warshall(n, edges))))
    weighted = [(u, v, rng.randrange(-8, 9)) for u, v, w in edges]
    result = bf.bellman_ford(n, weighted, s)
    add('bell', [n, len(weighted), s, *flat(weighted)], ['NEG'] if result is None else dist(result))
    undirected = [(w, u, v) for u, v, w in weighted]
    cost, chosen = mst.kruskal(n, undirected)
    add('mst', [n, len(undirected), *flat(undirected)], [cost, len(chosen)])

for n in (0, 1, 2, 7, 30):
    a = [rng.randrange(-30, 31) for _ in range(n)]
    initial, args, expected = a[:], [], []
    for _ in range(100):
        if n and rng.random() < .5:
            i, x = rng.randrange(n), rng.randrange(-50, 51)
            args.extend((0, i, x)); a[i] = x
        else:
            l, r = sorted((rng.randrange(n + 1), rng.randrange(n + 1)))
            args.extend((1, l, r)); expected.append(sum(a[l:r]))
    add('seg', [n, 100, *initial, *args], expected)
    a, args, expected = [0] * n, [], []
    for _ in range(100):
        l, r = sorted((rng.randrange(n + 1), rng.randrange(n + 1)))
        if rng.random() < .5:
            x = rng.randrange(-20, 21); args.extend((0, l, r, x))
            for i in range(l, r):
                a[i] += x
        else:
            args.extend((1, l, r)); expected.append(sum(a[l:r]))
    add('lazy', [n, 100, *args], expected)
for _ in range(25):
    values = [rng.randrange(25) for _ in range(60)]
    queries, expected = [], []
    for _ in range(30):
        l = rng.randrange(len(values)); r = rng.randrange(l + 1, len(values) + 1); k = rng.randrange(1, r - l + 1)
        queries.append((l, r, k)); expected.append(sorted(values[l:r])[k - 1])
    add('pst', [25, len(values), len(queries), *values, *flat(queries)], expected)
    lines = [(rng.randrange(-20, 21), rng.randrange(-50, 51)) for _ in range(40)]
    xs = sorted(rng.randrange(-100, 101) for _ in range(40))
    add('cht', [len(lines), len(xs), *flat(lines), *xs], flat([(max(a*x+b for a,b in lines),)*2 for x in xs]))

scc, bcc = load('Graph2/SCC'), load('Graph2/BCC')
dinic, costflow, matching = load('Graph2/Dinic'), load('Graph2/MCMF'), load('Graph2/Hopcroft')
for _ in range(60):
    n = rng.randrange(2, 9)
    edges = [tuple(rng.sample(range(n), 2)) for _ in range(14)]
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
    comp, groups = scc.strongly_connected_components(graph)
    add('scc', [n, len(edges), *flat(edges)], [int(comp[u] == comp[v]) for u in range(n) for v in range(n)])
    cuts, bridges, groups = bcc.biconnected_components(n, edges)
    add('bcc', [n, len(edges), *flat(edges)], [sum(1 << v for v in cuts), sum(1 << e for e in bridges), *vec(sorted(sum(1 << v for v in group) for group in groups))])
    weighted = [(u, v, rng.randrange(6)) for u, v in edges]
    network = dinic.Dinic(n)
    for edge in weighted:
        network.add_edge(*edge)
    add('flow', [n, len(weighted), *flat(weighted)], [network.max_flow(0, n - 1), 0])
    dag = [(u, v, rng.randrange(4), rng.randrange(-6, 7)) for u in range(n) for v in range(u + 1, n) if rng.random() < .6]
    network = costflow.MinCostFlow(n)
    for edge in dag:
        network.add_edge(*edge)
    limit = rng.randrange(10)
    add('cost', [n, len(dag), limit, *flat(dag)], network.run(0, n - 1, limit))
    graph = [[u for u in range(7) if rng.random() < .4] for _ in range(n)]
    edges = [(v, u) for v in range(n) for u in graph[v]]
    le, ri, cover = matching.hopcroft_karp(graph, 7)
    add('match', [n, 7, len(edges), *flat(edges)], [sum(u != -1 for u in le)])
add('bcc', [3, 0], [0, 0, *vec([1, 2, 4])])
add('cost', [2, 2, 1, 0, 0, 1, -1, 0, 1, 1, 0], ['NEG'])
add('flow', [3000, 2999, *flat((i, i + 1, 7) for i in range(2999))], [7, 0])
LCA, HLD = load('Graph2/LCA').LCA, load('Graph2/HLD').HLD
for n in (1, 2, 15, 150, 3000):
    edges = [(v, v - 1 if n == 3000 else rng.randrange(v)) for v in range(1, n)]
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v); graph[v].append(u)
    lca, hld = LCA(graph), HLD(graph)
    values = [0] * n
    for v in range(n):
        values[hld.pos[v]] = v + 1
    queries = [(rng.randrange(n), rng.randrange(n)) for _ in range(60)]
    expected = []
    for u, v in queries:
        l, r = hld.subtree_range(u)
        expected.extend((lca.query(u, v), sum(sum(values[a:b]) for a,b in hld.path_ranges(u,v)),
                         sum(sum(values[a:b]) for a,b in hld.path_ranges(u,v,True)), sum(values[l:r])))
    add('tree', [n, len(queries), *flat(edges), *flat(queries)], expected)

crt = load('Math/ChineseRemainderTheorem').crt
for _ in range(80):
    equations = [(rng.randrange(-100, 101), rng.randrange(1, 40)) for _ in range(rng.randrange(5))]
    out = crt(equations)
    add('crt', [len(equations), *flat(equations)], ['NONE'] if out is None else out)
for n in (0, 1, 2, 200, 1000):
    primes, spf, phi, mu, tau, sigma = load('Math/LinearSieve').linear_sieve(n)
    add('sieve', [n], vec(primes) + flat(zip(spf, phi, mu, tau, sigma)))
mr = load('Math/MillerRabin-PollardRho')
for n in [1,2,3,4,341550071728321,1000000007*1000000009,18446744073709551557,2**64-1] + [rng.randrange(1,1000000) for _ in range(50)]:
    factors = mr.factorize(n)
    add('prime', [n], [int(mr.is_prime(n)), len(factors), *flat(factors)])
matrix = load('Math/Matrix')
for _ in range(50):
    n, m = rng.randrange(1, 6), rng.randrange(1, 6)
    a = [[rng.randrange(-10, 11) for _ in range(m)] for _ in range(n)]
    rref, rank, determinant, inverse = matrix.gauss(a, 101)
    add('matrix', [n,m,101,*flat(a)], [rank, 'NONE' if determinant is None else determinant, *flat(rref), *(['NONE'] if inverse is None else ['INV',*flat(inverse)])])
add('real', [], ['OK'])
for _ in range(60):
    a = [rng.randrange(-200, 201) for _ in range(rng.randrange(0, 30))]
    b = [rng.randrange(-200, 201) for _ in range(rng.randrange(0, 30))]
    mod = rng.choice([1, 998244353, 1000000007, 2147483647])
    out = [0] * (len(a)+len(b)-1) if a and b else []
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j] += x*y
    add('conv', [len(a),len(b),mod,*a,*b], vec([x%mod for x in out]) + vec(out))
for kind in '^|&':
    for _ in range(15):
        n=16; a=[rng.randrange(-10,11) for _ in range(n)]; b=[rng.randrange(-10,11) for _ in range(n)]
        out=[0]*n
        for i,x in enumerate(a):
            for j,y in enumerate(b):
                out[{'^':i^j,'|':i|j,'&':i&j}[kind]]+=x*y
        add('bitconv',[n,kind,*a,*b],vec(out))
KMP,Z,MA,SA,HASH = [load('String/'+name) for name in ('KMP','Z','Manacher','SuffixArray','Hashing')]
for _ in range(80):
    s=''.join(rng.choice('ab#') for _ in range(rng.randrange(35)))
    p=''.join(rng.choice('ab#') for _ in range(rng.randrange(6)))
    sa,lcp=SA.suffix_array(s); h=HASH.Hashing(s)
    expected=vec(KMP.kmp(s,p))+vec(Z.z_function(s))+vec(MA.manacher(s))+vec(sa)+vec(lcp)
    expected += [h.get(l,r) for l in range(len(s)+1) for r in range(l,len(s)+1)]
    add('strings',[json.dumps(s),json.dumps(p)],expected)

HULL,CAL,POLAR,PIP,PICP,SEG = [load('Geometry/'+x) for x in ('ConvexHull','Calipers','PolarSort','PointInPolygon','PointInConvexPolygon','SegmentIntersection')]
for _ in range(80):
    points=[(rng.randrange(-20,21),rng.randrange(-20,21)) for _ in range(rng.randrange(20))]
    h=HULL.convex_hull(points); pair=CAL.calipers(h)
    far='NONE' if pair is None else sum((x-y)**2 for x,y in zip(*pair))
    queries=[(rng.randrange(-25,26),rng.randrange(-25,26)) for _ in range(15)]
    expected=[len(h),*flat(h),far,*flat(POLAR.polar_sort(points))]
    expected += flat((int(PIP.point_in_polygon(h,p)),int(PICP.point_in_convex_polygon(h,p))) for p in queries)
    add('geometry',[len(points),len(queries),*flat(points),*flat(queries)],expected)
for _ in range(150):
    points=[(rng.randrange(-4,5),rng.randrange(-4,5)) for _ in range(4)]
    kind,p=SEG.segment_intersection(*points)
    expected=[kind]
    if kind==1:
        expected += [f'{Fraction(x).numerator}/{Fraction(x).denominator}' for x in p]
    add('intersection',flat(points),expected)
for _ in range(50):
    values=[rng.randrange(-20,21) for _ in range(rng.randrange(50))]
    add('lis',[len(values),*values],vec(load('Misc/LIS').lis(values)))
for values in ([],[-2**63,2**63-1,0,-1,12345],list(range(-10000,10000))):
    add('io',[json.dumps(' '.join(map(str,values)))],vec(values))

print(f'Running {len(cases)} cross-language cases...', flush=True)
process = subprocess.run([str(runner)], input='\n'.join(cmd for op,cmd,out in cases)+'\n',
                         text=True, capture_output=True, timeout=120)
if process.returncode:
    raise AssertionError(f'C++ runner failed ({process.returncode}): {process.stderr[-3000:]}')
actual=process.stdout.splitlines()
assert len(actual)==len(cases),(len(actual),len(cases),process.stderr)
for index,((op,command,expected),line) in enumerate(zip(cases,actual)):
    if line.split()!=expected.split():
        raise AssertionError(f'Case {index} {op}\n{command[:2000]}\nExpected {expected[:2000]}\nActual {line[:2000]}')
report={'compiler':subprocess.check_output([compiler,'--version'],text=True).splitlines()[0],
        'flags':flags,'seed':20261014,'standalone_cpp_headers':len(headers),
        'differential_cases':len(cases),'cases_by_operation':dict(collections.Counter(op for op,_,_ in cases)),
        'status':'passed','online_judge':'not run','maximum_input_benchmark':'not run'}
(ROOT/'mixed/validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
