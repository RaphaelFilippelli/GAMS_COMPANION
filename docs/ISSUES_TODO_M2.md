# ISSUES_TODO_M2.md — Copy each section into a GitHub Issue

## P0: UI — Scenario field + recent list
**Why**: Make scenarios first-class without changing main flow.
**What**:
- Add a text input + file picker for "Scenario YAML (optional)" on the Run page.
- Remember last 5 entries in `.app_state/scenario_recent.json`.
- Pass `scenario_yaml` to `run_gams(...)`.
**Acceptance**: User can browse to a YAML and run; `debug_paths.json` contains `scenario_yaml`.
**Owner**: Claude Code
**Files**: `src/app/main.py` (or a small new page)

---

## P0: Batch + KPI CLI
**Why**: Explore many scenarios quickly.
**What**:
- `tools/kpis.py` to extract KPIs from `results.duckdb` (or fallback GDX).
- `tools/run_matrix.py` reads `--scenarios` dir or list, optional `--kpis kpis.yaml`.
- Writes `runs/matrix_summary.csv/json` with one row per run + KPI columns.
**Acceptance**: Running 3 scenarios yields a summary with KPI numbers.
**Owner**: Claude Code
**Files**: `tools/kpis.py`, `tools/run_matrix.py`

---

## P1: Compare Runs v1.1
**Why**: Deltas often need outer join and XLSX.
**What**:
- Add “Join type: inner/outer” select.
- Add “Export to XLSX” using `openpyxl`.
**Acceptance**: User can export a wide table to Excel in one click.
**Owner**: Claude Code
**Files**: `src/app/pages/20_Compare_Runs.py`

---

## P1: KPI presets example
**Why**: Reuse KPIs across projects.
**What**:
- `docs/kpis_example.yaml` with 3–5 KPIs.
- Document how to refer to key columns (key1..key7) and filters.
**Owner**: Assistant
**Files**: `docs/kpis_example.yaml`, `docs/QUICKSTART_M2.md` (appendix)