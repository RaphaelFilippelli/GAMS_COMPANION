# Milestone 2 — Scenario Library, Compare Runs, Batch Runner

**Status:** Milestone 1 complete (all 6 tasks done). This milestone focuses on workflows users need daily:
1) Define, save, and re-use **scenarios** (parameter/scalar/set/equation tweaks).
2) **Compare runs** quickly and export deltas for reports.
3) Run **batches / matrices** of scenarios to explore sensitivities.

## Why these three?
- They unlock repeatability and collaboration.
- They minimize “clickops” in the UI and create a durable library for future papers and deliverables.
- They fit naturally on top of the existing runner + DuckDB/Excel outputs.

## Success criteria
- Scenario YAMLs are validated, diffable, and versioned in git.
- Compare page shows deltas for any symbol in seconds and exports a tidy CSV/XLSX.
- Batch runner executes N scenarios with provenance and writes a small summary table.

## Plan (1–2 PRs each, small diffs)
- **T-007 — Scenario schema + load/apply (v1)**  
  - Spec + validator + CLI: `tools/scenario.py`  
  - Apply flow: write `patch.gdx` + optional equation includes in temp workspace before run.
  - UI: “Scenario” selector in sidebar (optional for v1).

- **T-008 — Compare Runs page (v1)**  
  - New Streamlit page; select two `runs/<stamp>/` and a symbol; compute deltas (inner join on keys) and show table.
  - Export “diff” as CSV/Excel.

- **T-009 — Batch runner (v1)**  
  - CLI: `tools/run_matrix.py` (reads a list of scenarios or a grid), runs sequentially, writes `matrix_summary.csv` with run_id, scenario_id, objective(s), key KPIs.
  - (Optional) UI tab to trigger batch with a small YAML.

## Owners (suggested)
- Rapha: review/merge; provide 1–2 target symbols to test Compare page.
- Assistant: ship Compare Runs page (now) + specs + skeletons.
- Claude (when available): implement scenario apply + batch CLI per specs.
