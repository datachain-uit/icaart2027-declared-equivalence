#!/usr/bin/env python3
"""Figure 2: declarative rules changed per transition, by operator.

Input : <outdir>/adapter_changes_by_operator.csv (written by adapter_change_analysis.py)
Output: <outdir>/fig2-adapter-changes.pdf
Usage : python3 scripts/make_fig2_adapter_changes.py [outdir]   (default: results)
"""
import csv, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, 'results')
rows = list(csv.DictReader(open(os.path.join(out, 'adapter_changes_by_operator.csv'))))
order = ['REORDER_FIELDS', 'RENAME_FIELD', 'MOVE_PATH', 'CHANGE_OPTIONALITY', 'CHANGE_TYPE',
         'CHANGE_STRING_NORMALIZATION', 'CHANGE_DATE_FORMAT', 'CHANGE_COLLECTION_REPRESENTATION',
         'ADD_FIELD', 'REMOVE_FIELD']
labels = {'REORDER_FIELDS': 'reorder fields', 'RENAME_FIELD': 'rename field', 'MOVE_PATH': 'move path',
          'CHANGE_OPTIONALITY': 'change optionality', 'CHANGE_TYPE': 'change type',
          'CHANGE_STRING_NORMALIZATION': 'change string policy', 'CHANGE_DATE_FORMAT': 'change date format',
          'CHANGE_COLLECTION_REPRESENTATION': 'change collection repr.', 'ADD_FIELD': 'add field',
          'REMOVE_FIELD': 'remove field'}
by = {r['operator']: r for r in rows}
fig, ax = plt.subplots(figsize=(3.3, 2.35))
y = list(range(len(order)))[::-1]
left = [0] * len(order)
for key, name, col in [('m_map', 'mapping rule', '#4c72b0'), ('m_canon', 'normalization rule', '#dd8452'),
                       ('m_struct', 'structural rule', '#55a868')]:
    vals = [int(by[o][key]) for o in order]
    ax.barh(y, vals, left=left, color=col, label=name, height=0.62)
    left = [l + v for l, v in zip(left, vals)]
for yi, o in zip(y, order):
    n = by[o]['n']
    txt = f"n={n}"
    ax.text(int(by[o]['rules_total']) + 0.06, yi, txt, va='center', fontsize=6.5, color='#333333')
ax.set_yticks(y); ax.set_yticklabels([labels[o] + (' *' if by[o]['changes_a0_relation'] == 'yes' else '') for o in order], fontsize=7)
ax.set_xlim(0, 2.9); ax.set_xticks([0, 1, 2]); ax.tick_params(axis='x', labelsize=7)
ax.set_xlabel('declarative rules changed per transition', fontsize=7)
handles, names = ax.get_legend_handles_labels()
fig.legend(handles, names, fontsize=6.5, loc='upper center', bbox_to_anchor=(0.5, 1.0), ncol=3,
           frameon=False, handlelength=1.2, columnspacing=0.9)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(os.path.join(out, 'fig2-adapter-changes.pdf'))
print('wrote fig2-adapter-changes.pdf')
