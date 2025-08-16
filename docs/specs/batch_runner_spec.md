# Batch Runner — Spec (v1)

## Goal
Run a list (or grid) of scenario YAMLs sequentially, each producing a run folder with `raw.gdx`, `.lst`, `run.json`.
Write a lightweight summary JSON/CSV at the end.

## Inputs
- Model folder, main.gms, expected gdx_out
- Scenarios: a folder with *.yaml or a YAML file listing paths

## Output
- `runs/matrix_summary.json` — array of {scenario, run_dir, gdx}

## v2 ideas
- Concurrency with a worker pool (watch CPU/RAM); retries on failure
- KPI extraction (read values for configured symbols into the summary)
