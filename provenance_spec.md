# Provenance & Reproducibility

Each run folder stores `run.json`:

```jsonc
{
  "run_id": "01J9M...",
  "timestamp": "2025-08-12T21:37:12Z",
  "scenario_id": "pmodel_baseline_v1",
  "gams": {"home": "C:/GAMS/44", "version": "44.1.0", "options": {"Lo": 2, "gdxcompress": 1}},
  "model": {"work_dir": "C:/Models/PModel", "main": "main.gms", "hash": "<sha256>"},
  "patch": {"hash": "<sha256>", "symbols": ["Penalty1", "ActiveMeasures"]},
  "git": {"commit": "a1b2c3", "dirty": false}
}
```

### How hashes are computed
- **model.hash**: sorted list of file paths + bytes (excluding `runs/`) → SHA256.
- **patch.hash**: bytes of `patch.gdx` → SHA256.

Embed a compact version of this JSON as a hidden sheet in Excel exports.
