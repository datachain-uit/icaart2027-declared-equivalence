# Data files

All files come from the measurements and the benchmark described in the paper. Values are unchanged.
The tables keep the columns needed to recompute the paper's numbers. All data are synthetic.

| File | Content | SHA-256 |
|---|---|---|
| `adapter-changes.csv` | One row per retained schema transition and the initial adapter (3,547 rows) | `e5aca7bb6c084dfea519014918444598306e88a73e7ba2fd0fbe7d80588a1fb8` |
| `conformance.csv` | Conformance battery per property and class (36 rows) | `804bed1e7d43728766e6bbb43c44800e06a6876909432a73fb31a5fcaa9af3f5` |
| `differential-pairs.csv` | Differential divergences of the reproduced SB pipeline in the comparable classes (600 rows) | `3888b81503d3609dbd3b59f4eb032e39733d5d2bba36db6c39da4490fcbdeecd` |
| `decision-cases.csv` | The three off-chain decision cases reported in the paper | `ac3df458a5cefd0b5ea10352f20a6b4223dbdaa36ce96fb08f6231b45e3adb5f` |
| `per-record-timing.csv` | Per-record timings of EXT at Merkle depth 11 (medians and quartiles, ms) | `7f35e32d675eb2b43029f93684c7b342549cdb6ef0cf0d65dfd4113bf70a85de` |
| `gas/summary_by_operation.csv` | Gas per operation, back-end and network over the 80 runs | `4e8c5866eaebfc3ba1adb37d20633d3d13778f0cddc4721f5ec5bf5734964eff` |
| `gas/manager_deploy_normalisation.csv` | Manager deployment gas per run, with constructor zero bytes | `445ee987ba1c7686d68e3cf544e3928c9119d3d1a82b5715a5174f613bcbbdac` |
| `gas/evm_per_proof.csv` | EVM verification gas per proof with calldata and re-execution terms | `0bd2ca478a827b5852faa72c9c58ab5c1d10b68eebe2707bc5d4ad922b23db46` |
| `gas/reexecution.csv` | ethereumjs re-execution of the eight proofs per back-end | `a9959dd16b2d6f5b622c6a207a9c4dbee6baed77df8c1ee78efb4421763510b9` |
| `gas/zksync_sessions_levels.csv` | zkSync Era Sepolia gas levels per session and operation | `b262c9842fc51abe9b6ab19fee3bf382e0add771917a77675ed2e93c65c2e33e` |
| `gas/zksync_value_levels.csv` | zkSync Era Sepolia session S3 value counts | `62232620be76b7c4060fb4e78ff1b8b9bce7b356e87daf3bb79128782837d8a7` |
| `gas/zksync_elevated_transactions.csv` | zkSync Era Sepolia transactions above the session level | `5ea8418d4d57ab21a22881d1dbbee89f251f238fe09a6fb70df78acfdf3068ca` |

In the gas tables, `environment` is `hardhat` (local chain), `sepolia` (Ethereum Sepolia) or
`zkSyncSepolia` (zkSync Era Sepolia), and all values are gas used. In the other tables, `A0` denotes the
schema-bound baseline (SB) and `A1` the external-interpretation design (EXT).
