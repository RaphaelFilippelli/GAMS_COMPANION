
# Compare Runs — Spec (v1)

## Goal
Let a user pick two completed runs, choose a symbol, and see the **difference**:
- Inner join on all key columns (key1..key7), compute `delta = value_B - value_A` and `%delta`.
- Show top N rows, filter, and export to CSV/XLSX.

## Inputs
- Two run folders under `runs/`.
- Selected symbol name (must exist in both runs).

## Implementation details
- Read DuckDB if present; else read GDX and normalize to 7 key columns.
- Use Pandas for now (fast enough for small/medium runs).

## Output columns
`key1..key7, value_A, value_B, delta, pct_delta` (+ optionally text columns if present).

## Edge cases
- Missing rows: use inner join for v1; future v2 may add outer join with fillna.
- Multi-dim symbols: handle generically via key1..key7 columns.
- Units: optional; can show unit string if provided in meta later.
