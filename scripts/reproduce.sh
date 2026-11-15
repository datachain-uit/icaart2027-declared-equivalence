#!/usr/bin/env bash
# Regenerates the derived tables into a temporary directory and compares them byte for byte
# with the committed files in results/. Exit status 0 means every table was reproduced exactly.
set -euo pipefail
cd "$(dirname "$0")/.."
tmp="$(mktemp -d)"
python3 scripts/adapter_change_analysis.py "$tmp" > /dev/null
python3 scripts/divergence_analysis.py "$tmp" > /dev/null
status=0
for f in adapter_changes_by_operator.csv adapter_changes_by_sequence.csv divergences_by_class.csv conformance_summary.csv; do
  if cmp -s "$tmp/$f" "results/$f"; then echo "identical  $f"; else echo "DIFFERENT  $f"; status=1; fi
done
if python3 -c "import matplotlib" 2>/dev/null; then
  python3 scripts/make_fig2_adapter_changes.py "$tmp" > /dev/null && echo "figure     $tmp/fig2-adapter-changes.pdf (compare visually with results/)"
fi
exit $status
