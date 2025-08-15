**Role:** Implementer + Reviewer

**Goal:** Finish `run-scenario` so I can run a whole scenario YAML (edits + equation includes) from the command line, with a “compile-only” mode and a clean results package.

**Read first:**

* `docs/agents.md`
* `docs/scenario_spec.md` (from earlier you already have; if missing I can re-share)
* `docs/cli_spec.md`
* `docs/provenance_spec.md`
* `docs/results_schema.md`
* `docs/gams_integration.md`

**Where to code:**

* Update `src/cli.py`
* Add new helpers under `src/core/`:

  * `patch_builder.py` — build `patch.gdx` from scenario edits (scalars/params/sets), reading CSVs for parameters.
  * `equation_injector.py` — in a temp copy of the model, inject `$include` lines listed in the scenario.
  * `provenance.py` — write `run.json` per `provenance_spec.md`.

**What “Done” means (acceptance criteria):**

1. `python -m src.cli run-scenario toy_model/scenario_baseline.yaml --dry-run` compiles without solving and writes logs.
2. Running without `--dry-run` solves and creates a new folder under `runs/` containing:

   * `raw.gdx`
   * `run.json` with hashes and options
   * `…_results.xlsx` (Excel export)
3. Parameter CSV overlays work (e.g., `edits/cost_by_catchment.csv`).
4. Equation include file is injected and effective (limits `x('A') <= 3` in toy model).
5. Code passes `ruff check .` and `pytest -q`.
6. Update `docs/tasks_backlog.md` task T-001 → DONE.

**Tests to add (minimal):**

* `tests/test_cli_run_scenario.py`:

  * dry-run returns non-error exit and creates a run folder with `.lst`.
  * normal run creates `raw.gdx` + Excel.
  * modified CSV changes a result cell (assert difference).