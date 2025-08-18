# Roadmap to v1.0 — GAMS Companion

## Reflection (where we are)
- ✅ Temp‑isolated runs via Control API; Transfer API for I/O
- ✅ Robust Excel & DuckDB exports
- ✅ Compare Runs page
- ✅ LO handling clarified (API vs CLI)
- ✅ Scenario engine (builds `patch.gdx`, optional includes) — ready to integrate in UI
- ⏳ Async path exists in your main app; stable for non‑scenario runs

## Finish line (v1.0) — what “done” means
1) **Scenario-first workflow**: pick or compose a scenario → run → results saved with provenance (`run.json`, Excel/DB).
2) **Batch exploration**: run a folder/list of scenarios and produce a KPI summary for quick triage.
3) **Analysis**: Compare Runs with inner/outer join and easy CSV/XLSX export; KPI charts.
4) **Reporting**: One-click “Export pack” (Excel + selected charts + CSVs) suitable for papers/deliverables.
5) **Reliability**: Good errors, live logs, and a short “preflight check” page.
6) **Docs**: Quickstart & ops cookbook for collaborators.

## Milestones
### M2 — Scenarios & Batch (current)
- UI: Scenario YAML path field & recent list (file picker) [P0]
- Batch CLI with KPI extraction to CSV/JSON [P0]
- Compare v1.1: outer join toggle + XLSX export [P1]
- KPI presets file (YAML) for paper deliverables [P1]

### M3 — Analysis & Reporting
- Chart presets (Plotly) + export PNG/SVG [P0]
- “Export Pack” (zip): Excel, CSV diffs, charts, provenance [P0]
- Notebook template (.ipynb) seeded from a run [P1]

### M4 — Model editing helpers (safe)
- Scenario editor (GUI) to compose scalars/params/sets edits [P0]
- Include manager for equation snippets [P1]

### M5 — Reliability & polish
- Preflight page (GAMS version/API check, permissions, disk space) [P0]
- Large GDX streaming & caching (optional) [P1]
- CI: run Transfer-only tests; style & type checks [P1]

## Roles
- **Rapha**: reviews/merges; picks KPI symbols; provides 1–2 real scenarios.
- **Claude Code**: M2 UI wiring (scenario field), Batch+KPI CLI, Compare v1.1.
- **Assistant (me)**: Design specs, KPI extractor module, ready-to-run pages, docs, surgical patches on request.

## Acceptance tests (v1.0)
- Can run 3 scenarios and get: `raw.gdx`, `.lst`, `run.json`, `results.xlsx`, `results.duckdb`.
- Compare two runs for symbol X, export diff to CSV, and paste into a paper figure.
- Batch 10 scenarios with a KPI preset; open `matrix_summary.csv` and see the KPI table.
- “Export pack” produces a zip with provenance and charts for one scenario.