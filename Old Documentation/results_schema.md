# Results Schema

Standardized tables written to DuckDB per run.

## Tables
### `meta_run`
| column | type | description |
|--------|------|-------------|
| run_id | TEXT | unique ULID |
| timestamp | TIMESTAMP | run start time |
| gams_version | TEXT | e.g., 44.1.0 |
| model_hash | TEXT | SHA256 of model tree |
| patch_hash | TEXT | SHA256 of patch.gdx |
| commit | TEXT | git commit (if available) |
| scenario_id | TEXT | from scenario.yaml |

### `symbol_values`
Long, tidy layout for all numeric symbols (parameters, variables levels).

| column | type | notes |
|--------|------|------|
| run_id | TEXT | FK → meta_run |
| symbol | TEXT | e.g., `ReducedP` |
| kind | TEXT | `parameter|variable|equation` |
| dim | INT | arity (0–10) |
| k1..k7 | TEXT | UELs (nullable) |
| value | DOUBLE | numeric |
| text | TEXT | annotations (nullable) |

### `symbol_marginals`
Optional duals/marginals for variables/equations.

| column | type |
|--------|------|
| run_id | TEXT |
| symbol | TEXT |
| k1..k7 | TEXT |
| marginal | DOUBLE |

## Excel Export
- One worksheet per symbol **and** a `meta` sheet mirroring `meta_run`.
- Column order: keys → value → text.
- Freeze header; include units in header if provided.
