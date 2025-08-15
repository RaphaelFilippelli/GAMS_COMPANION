# CLI Specification

Package name: `gams_helper` (exposed as `python -m gams_helper`)

## Commands
### `init`
Scan a model directory and write `symbol_index.json` and a template `scenario.yaml`.

### `run-scenario`
```
python -m gams_helper run-scenario path/to/scenario.yaml [--dry-run] [--out runs/]
```
- Builds `patch.gdx` from edits.
- Injects equation includes.
- If `--dry-run`, compiles only (no solve), still writes logs.
- On success, writes `raw.gdx`, DuckDB, Excel, plots, `run.json` (provenance).

### `export`
```
python -m gams_helper export --gdx raw.gdx --excel results.xlsx --duck runs/run.duckdb
```
Re-exports without re-running GAMS.

### `queue`
Simple local job queue to serialize runs (avoid file locks).

## Exit Codes
- `0` success
- `2` compile error
- `3` solve error
- `4` export error
