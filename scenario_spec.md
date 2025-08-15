# Scenario Manifest — `scenario.yaml`

A portable description of a model run. Check into git for provenance.

```yaml
id: pmodel_baseline_v1
description: Baseline run for Nov 2025
model:
  work_dir: C:/Models/PModel
  main_file: main.gms
gams:
  options:
    Lo: 2
    gdxcompress: 1
edits:
  scalars:
    Penalty1: 1000        # numeric
  parameters:
    # CSV file with columns: key1,key2,...,value
    CostByCatchment: edits/cost_by_catchment.csv
  sets:
    ActiveMeasures:
      add: [FO, LRl]
      remove: [OldMeasure]
equations:
  # optional include patches (see equation_patches/)
  - file: equation_patches/new_constraint.inc
notes: |
  Any free-text notes about rationale or links.
```

## Rules
- **Only** specify changes; unspecified symbols inherit defaults from the template GDX/model.
- All referenced CSVs must be relative to the scenario file location.
- On run, the app creates a `patch.gdx` from `edits.*` and injects any `equations` includes.
