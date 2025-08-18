# FINISH_LINE.md — Definition of Done for v1.0

1) **Runs**
   - Runs execute in a temp workspace, never mutate source.
   - Artifacts: `raw.gdx`, `.lst`, `run.json`, `results.xlsx`, `results.duckdb`, `debug_paths.json`.
2) **Scenarios**
   - YAML schema validated; scenario applied automatically (patch.gdx + optional includes).
   - UI field + recent list; can run with/without scenario.
3) **Batch**
   - CLI runs a folder/list of scenarios, writes `matrix_summary.csv/json` with KPIs.
4) **Analysis**
   - Compare Runs does inner/outer join and exports to CSV/XLSX.
5) **Reporting**
   - Export Pack zip contains Excel, selected CSV/plots, and provenance sheet.
6) **Docs**
   - Quickstart, Scenario quickstart, KPI presets example, Batch CLI usage.
7) **Reliability**
   - Preflight passes on a clean Windows 11 machine with GAMS v49+.