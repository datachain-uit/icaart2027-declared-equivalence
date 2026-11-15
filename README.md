# Declared Equivalence for Privacy-Preserving Verification under Schema Evolution: data and analysis

This repository contains the data and the analysis scripts behind the numbers reported in

> Khoa Tan Vo, Hong-Tri Nguyen and Tu-Anh Nguyen-Hoang. *Interpreting Structured Records Outside the
> Proof: Declared Equivalence for Privacy-Preserving Verification under Schema Evolution.* In Proceedings
> of the 19th International Conference on Agents and Artificial Intelligence (ICAART 2027), SCITEPRESS.

The paper compares two pipelines for zero-knowledge membership verification of structured records:

- **EXT** (external interpretation): a declarative, invariant-checked adapter interprets the record and
  the proof establishes only schema-independent membership. In the data files this design is labelled
  `A1`.
- **SB** (schema-bound baseline): a fixed-slot credential circuit whose relation depends on the field
  structure. In the data files this design is labelled `A0` (for example `differential_a0`,
  `changes_a0_relation`).

Class identifiers such as `unicode-normalisation` are kept exactly as they appear in the data. The optional-states class and the two array classes are undefined for SB, which has no source-level encoding for absent or null values or for arrays, so they are not part of the differential comparison.

## Reproduce

Requirements: Python 3.8 or later. The figure additionally needs matplotlib.

```bash
bash scripts/reproduce.sh
```

The script recomputes the four derived tables into a temporary directory and compares them byte for byte
with the files in `results/`. It prints `identical` for each table that is reproduced exactly and exits
with status 0. It also regenerates Figure 2 for visual comparison.

## Contents

| Path | What it is | Used for |
|---|---|---|
| `data/adapter-changes.csv` | One row per retained schema transition (3,546) and the initial adapter: operator, sequence seed, changed mapping (`m_map`), normalization (`m_canon`) and structural (`m_struct`) rules, generated tests (`m_test`), changed configuration lines (`m_loc`) | Section 5.2, Figure 2 |
| `data/conformance.csv` | Conformance battery per property and class: cases run, passed, divergences; differential rows for the reproduced SB pipeline (classes SB can encode, plus the two array classes marked undefined) | Section 5.1, Table 2 |
| `data/differential-pairs.csv` | The 600 differential divergences in the comparable classes, with both inputs of each pair | Section 5.1, Table 2 |
| `data/decision-cases.csv` | The three off-chain decision cases reported in the paper | Section 5.1 |
| `data/per-record-timing.csv` | Per-record timings of EXT (`A1`) at Merkle depth 11, Groth16 and PLONK: medians and quartiles in ms | Section 5.2 |
| `data/gas/*.csv` | Derived gas tables of the 80 measurement runs: per operation and network, per proof on the EVM path with calldata and re-execution, zkSync Era sessions and first-transaction excesses | Section 5.3 |
| `scripts/adapter_change_analysis.py` | Writes `adapter_changes_by_operator.csv` and `adapter_changes_by_sequence.csv` | |
| `scripts/divergence_analysis.py` | Writes `divergences_by_class.csv` and `conformance_summary.csv` | |
| `scripts/make_fig2_adapter_changes.py` | Draws Figure 2 | |
| `results/` | The derived tables and Figure 2 as used in the paper | |

## Where the paper's numbers come from

| Number in the paper | File and field |
|---|---|
| 6,802 direct cases; 2,600 / 1,600 / 260 / 200 / 2,142 | `results/conformance_summary.csv` (rows other than `differential_a0*`) |
| 2,000 comparable pairs, 1,400 agree, 600 diverge, 10 comparable classes | `results/conformance_summary.csv`, row `differential_a0_comparable` |
| 200 separations each for date-format, trim-policy and unicode-normalisation; no merges | `results/divergences_by_class.csv` |
| 3,546 transitions, 400 sequences, 11.3% zero-rule transitions, at most two rules, 8 to 11 rules per sequence (median 9), 22.6% field-count transitions | `results/adapter_changes_by_sequence.csv` |
| Rules and tests per operator, operator counts (Figure 2) | `results/adapter_changes_by_operator.csv` |
| 0.175 / 0.453 / 155.1 / 6.2 / 161.4 ms (Groth16); 0.223 / 0.489 / 9,511.7 ms (PLONK) | `data/per-record-timing.csv` |
| Verification gas ranges of 48 (Groth16) and 2,606 (PLONK, median 301,992) | `data/gas/summary_by_operation.csv`, `data/gas/evm_per_proof.csv`, `data/gas/reexecution.csv` |
| Three Sepolia manager deployments with one constructor zero byte | `data/gas/manager_deploy_normalisation.csv` |
| Session S3: 79 of 80 PLONK and 75 of 80 Groth16 verifications on two values 6 gas apart | `data/gas/zksync_value_levels.csv` |
| Session and first-transaction shifts on zkSync Era | `data/gas/zksync_sessions_levels.csv`, `data/gas/zksync_elevated_transactions.csv` |

Percentages in the paper are the shares in these files with one decimal. Order statistics are non-interpolated.

## Provenance

`data/PROVENANCE.md` describes every data file and gives its SHA-256 checksum.
All data are synthetic. No personal or real credential data are included.

## License

Code (`scripts/`) is released under the MIT License (`LICENSE`). Data and derived results (`data/`,
`results/`) are released under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

## Citation

Please cite the paper above. `CITATION.cff` contains the citation metadata.
