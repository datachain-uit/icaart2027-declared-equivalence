#!/usr/bin/env python3
"""Conformance and differential analysis (Section 5.1, Table 2).

Input : data/conformance.csv        per property and class: cases run, passed, divergences
        data/differential-pairs.csv the recorded divergences of the reproduced SB pipeline
Output: <outdir>/divergences_by_class.csv, <outdir>/conformance_summary.csv
The differential comparison covers the ten classes that SB can encode. The optional-states and the two
array classes are undefined for SB and are not part of the comparison. In the data, A0 denotes SB and
A1 denotes EXT.
Usage : python3 scripts/divergence_analysis.py [outdir]   (default: results)
"""
import csv, collections, os, sys
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, 'results')
os.makedirs(out, exist_ok=True)
div = list(csv.DictReader(open(os.path.join(base, 'data', 'differential-pairs.csv'))))
assert len(div) == 600
t = collections.Counter((d['ambiguity_class'], 'merge' if 'MERGES' in d['consequence'] else 'separate') for d in div)
with open(os.path.join(out, 'divergences_by_class.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['ambiguity_class', 'direction', 'cases', 'declared_condition', 'consequence_category', 'status', 'source'])
    for (c, d), n in sorted(t.items()):
        cond = next(x['conditions_held'] for x in div if x['ambiguity_class'] == c)
        cat = 'distinct logical values map to one commitment (collision of declared-distinct records)' if d == 'merge' \
              else 'equivalent representations map to different commitments (declared-equivalent record fails to verify)'
        status = 'compared'
        w.writerow([c, d, n, cond, cat, status, 'derived']); print(c, d, n, status)
pf = dict(t)
print('comparable: merge', sum(n for (c, d), n in pf.items() if d == 'merge'), 'separate', sum(n for (c, d), n in pf.items() if d == 'separate'))
conf = list(csv.DictReader(open(os.path.join(base, 'data', 'conformance.csv'))))
agg = collections.defaultdict(lambda: [0, 0, 0, 0])
for r in conf:
    a = agg[r['property']]; a[0] += 1; a[1] += int(r['cases_run']); a[2] += int(r['cases_passed']); a[3] += int(r['divergences'])
with open(os.path.join(out, 'conformance_summary.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['property', 'classes', 'cases_run', 'cases_passed', 'divergences', 'source'])
    for p, a in agg.items(): w.writerow([p] + a + ['derived']); print(p, a)
    comp = [r for r in conf if r['property'] == 'differential_a0' and r['comparison_status'] != 'undefined-under-A0']
    w.writerow(['differential_a0_comparable', len(comp), sum(int(r['cases_run']) for r in comp), sum(int(r['cases_passed']) for r in comp), sum(int(r['divergences']) for r in comp), 'derived'])
    print('differential_a0_comparable', len(comp), sum(int(r['cases_run']) for r in comp), sum(int(r['cases_passed']) for r in comp), sum(int(r['divergences']) for r in comp))
direct = sum(a[1] for p, a in agg.items() if p != 'differential_a0')
print('direct cases', direct, 'total', sum(a[1] for a in agg.values()), 'undefined classes',
      sum(1 for r in conf if r['comparison_status'] == 'undefined-under-A0'))
