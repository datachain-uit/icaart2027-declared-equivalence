#!/usr/bin/env python3
"""Adapter-change analysis (Section 5.2, Figure 2).

Input : data/adapter-changes.csv, one row per retained schema transition (and the initial adapter),
        with the changed mapping (m_map), normalization (m_canon) and structural (m_struct) rules,
        generated tests (m_test) and changed configuration lines (m_loc).
Output: <outdir>/adapter_changes_by_operator.csv, <outdir>/adapter_changes_by_sequence.csv
Order statistics are non-interpolated: Q_p = x_(floor(p (r-1))).
Usage : python3 scripts/adapter_change_analysis.py [outdir]   (default: results)
"""
import csv, collections, os, sys
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
src = os.path.join(base, 'data', 'adapter-changes.csv')
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, 'results')
os.makedirs(out, exist_ok=True)
rows = list(csv.DictReader(open(src)))
trans = [r for r in rows if r['operator'] != 'INITIAL']
assert len(trans) == 3546 and len({r['sequence_seed'] for r in trans}) == 400
def q(v, p):
    v = sorted(v); return v[int(p * (len(v) - 1))]
def rules(r): return int(r['m_map']) + int(r['m_canon']) + int(r['m_struct'])
byop = collections.defaultdict(list)
for r in trans: byop[r['operator']].append(r)
with open(os.path.join(out, 'adapter_changes_by_operator.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['operator', 'n', 'changes_a0_relation', 'm_map', 'm_canon', 'm_struct', 'rules_total',
                'rules_min', 'rules_max', 'm_test', 'm_loc', 'm_loc_min', 'm_loc_max', 'source'])
    for op, rs in sorted(byop.items()):
        tot = [rules(r) for r in rs]
        w.writerow([op, len(rs), 'yes' if op in ('ADD_FIELD', 'REMOVE_FIELD') else 'no',
                    q([int(r['m_map']) for r in rs], .5), q([int(r['m_canon']) for r in rs], .5),
                    q([int(r['m_struct']) for r in rs], .5), q(tot, .5), min(tot), max(tot),
                    q([int(r['m_test']) for r in rs], .5), q([int(r['m_loc']) for r in rs], .5),
                    min(int(r['m_loc']) for r in rs), max(int(r['m_loc']) for r in rs), 'derived'])
seqs = collections.defaultdict(list)
for r in trans: seqs[r['sequence_seed']].append(r)
cum = [sum(rules(r) for r in rs) for rs in seqs.values()]
lens = [len(rs) for rs in seqs.values()]
tot_all = [rules(r) for r in trans]
with open(os.path.join(out, 'adapter_changes_by_sequence.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['statistic', 'value'])
    for k, v in [('sequences', len(seqs)), ('transitions', len(trans)),
                 ('rules_per_sequence_min', min(cum)), ('rules_per_sequence_q1', q(cum, .25)),
                 ('rules_per_sequence_median', q(cum, .5)), ('rules_per_sequence_q3', q(cum, .75)),
                 ('rules_per_sequence_max', max(cum)), ('sequence_length_min', min(lens)),
                 ('sequence_length_max', max(lens)), ('rules_total', sum(tot_all)),
                 ('transitions_with_zero_rules', sum(1 for t in tot_all if t == 0)),
                 ('transitions_with_zero_rules_share', round(sum(1 for t in tot_all if t == 0) / len(tot_all), 4)),
                 ('rules_per_transition_max', max(tot_all)),
                 ('generated_tests_total', sum(int(r['m_test']) for r in trans)),
                 ('field_count_transitions', sum(len(byop[o]) for o in ('ADD_FIELD', 'REMOVE_FIELD'))),
                 ('field_count_transitions_share', round(sum(len(byop[o]) for o in ('ADD_FIELD', 'REMOVE_FIELD')) / len(trans), 4)),
                 ('initial_adapter_m_map', [r for r in rows if r['operator'] == 'INITIAL'][0]['m_map']),
                 ('initial_adapter_m_test', [r for r in rows if r['operator'] == 'INITIAL'][0]['m_test'])]:
        w.writerow([k, v]); print(k, v)
