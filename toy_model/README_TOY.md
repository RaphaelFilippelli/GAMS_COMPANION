# Toy GAMS Model (for tests)

This toy LP maximizes net benefit with a capacity limit and supports patching via `patch.gdx` and `$include`d equation files.

## Files
- `main.gms` — the model
- `scenario_baseline.yaml` — example scenario manifest
- `edits/cost_by_catchment.csv` — parameter override (key1,value)
- `equation_patches/new_constraint.inc` — example constraint

## How to run (manually)
1. Open a shell in this folder.
2. Run GAMS:
   ```
   gams main.gms Lo=2
   ```
3. Inspect `results.gdx` with your toolchain (`gdx_io.read_gdx`, `export_excel`, etc.).

## How to run (via app/CLI)
When the CLI is implemented:
```
python -m gams_helper run-scenario scenario_baseline.yaml --out ../../runs/
```
