1. Scenario matrix runner (sweeps)

* Add `matrix.yaml` to define ranges/lists of edits (e.g., `Cap: [6,8,10]`) and auto-fan-out into many scenario runs with a single command.
* Output a consolidated DuckDB table to compare across runs quickly.

2. Pydantic-validated configs

* Define pydantic models for `scenario.yaml` and `symbol_manifest.json`.
* You’ll get better error messages, defaulting, and auto-generated JSON schema.

3. Pandera validation for results

* Create a `pandera` schema for `symbol_values` to catch missing columns, bad types, or NaNs where they shouldn’t be.

4. Units & metadata

* Add `units` mapping in the manifest and propagate into Excel headers and Plotly axes.
* Let the UI attach “tags” or notes to each run (e.g., “baseline”, “Cap=8, A≤3”).

5. Batch-safe job queue

* A tiny local queue (or SQLite-backed) to serialize runs, avoid file locking, and throttle concurrency on Windows.

6. Remote runners

* Optional SSH/WinRM “runner” so heavy solves happen on a remote workstation or server, while the UI stays local.
* Provenance should capture remote environment details.

7. Pluggable exporters

* Define an `Exporter` interface and register plugins: `ExcelExporter`, `DuckDBExporter`, `LaTeXTableExporter`, `GeoPackageExporter` (if you ever output spatial).
* Makes it easy to add formats without touching the core pipeline.

8. Interactive “diff”—before you run

* In the UI: show a **diff view** of proposed edits vs. the template GDX (per symbol) and a “risk score” (e.g., changed set cardinalities).
* Great for catching accidental wide changes.

9. Guardrails for equation patches

* Pre-flight compile with `$exit` before solve; if it fails, show the exact offending line and fail fast.
* Keep a library of **lint rules** for your .inc patches (e.g., warn on undeclared symbols).

10. Result caching (content-hash)

* Cache exports keyed by `(model_hash, patch_hash, options)`.
* If nothing changed, skip re-solve and just re-export or reuse prior DuckDB.

11. Better logs & observability

* Structured logging (JSON logs) with run\_id correlation.
* A small “Run Monitor” page to tail the `.lst` file and show progress markers (compile/solve/export).

12. Paper-ready outputs

* Add LaTeX table generators (booktabs) and a “Copy as LaTeX” button.
* Plot styles: IEEE/Elsevier presets with consistent fonts and DPI; SVG default.

13. Access control / profiles (optional)

* Profiles for “Researcher” (can edit scalars/parameters) vs “Developer” (can patch equations).
* Simple role flag in a config file is enough.

14. API surface

* Add a fastAPI wrapper around the CLI so other tools (or notebooks) can trigger runs and fetch artifacts programmatically.

15. Golden datasets & CI artifacts

* Commit a tiny known-good `raw.gdx` + `results.xlsx` for the toy model and hash-check them in CI to detect regressions in the I/O layer.
